from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import RecipeForm, UserUpdateForm, UserProfileForm, FeedbackForm, ProfilePictureForm
from .models import Recipe, Review, Category, Like, UserProfile
from recipes import models

# Home page
def index(request):
    categories = Category.objects.all()
    featured_recipes = Recipe.objects.filter(is_featured=True)[:3]  # Get the top 3 featured recipes
    top_categories = Category.objects.all()[:3]  # Get the top 3 categories
    return render(request, 'recipes/index.html', {
        "categories": categories,
        'featured_recipes': featured_recipes,
        'top_categories': top_categories
    })

def about(request):
    return render(request, "recipes/about.html")

# User Authentication
def register(request):
    if request.method == "POST":
    
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        return redirect("login")
    else:
        return render(request, "recipes/register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "recipes/login.html", {"error": "Invalid credentials"})
    else:
        return render(request, "recipes/login.html")
    
@login_required
def user_logout(request):
    logout(request)
    return redirect("recipes:index")

@login_required
def profile_view(request):
    return render(request, "profile.html")

@login_required
def manage_account(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('recipes:user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'manage_account.html', {'form': form, 'user_profile': user_profile})

@login_required
def manage_account_view(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, "manage_account.html", {"form": form})

@login_required
def delete_account_view(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("home")
    
    return render(request, "profile.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("index")

@login_required
def delete_account(request):
    request.user.delete()
    logout(request)
    return redirect("recipes:index")


# Recipe Management
@login_required
def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect("recipes:recipe_detail", recipe.id)
    else:
        form = RecipeForm()
    
    return render(request, "recipes/create_recipe.html", {"form": form})

def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.select_related('author'), id=recipe_id)
    reviews = Review.objects.filter(recipe=recipe).select_related('user')
    return render(request, "recipes/view_recipe.html", {"recipe": recipe, "reviews": reviews})

@login_required
def edit_recipe(request, slug):
    print(f"Slug: {slug}")
    recipe = get_object_or_404(Recipe, slug=slug)

    # Ensure only the recipe author can edit the recipe
    if request.user != recipe.author:
        return redirect('recipes:view_recipe', slug=slug)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipes:view_recipe', slug=slug)
    else:
        form = RecipeForm(instance=recipe)

    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipes/edit_recipe.html', context)

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author == request.user:
        recipe.delete()
        return redirect("recipes:index")
    return redirect("recipes:view_recipe", recipe_id=recipe.id)


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect("recipes:index")

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipes:view_recipe", recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, "edit_recipe.html", {"form": form})


# Recipe Interactions
@csrf_exempt
@login_required
@require_POST
def like_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user

    if user in recipe.likes.all():
        recipe.likes.remove(user)
        liked = False
    else:
        recipe.likes.add(user)
        liked = True

    return JsonResponse({"liked": liked, "likes_count": recipe.likes.count()})


@login_required
@require_POST
def favorite_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)
    return JsonResponse({"success": True, "favorited": request.user in recipe.favorites.all()})

@login_required
@require_POST
def add_review(request, slug):
    rating = request.POST["rating"]
    comment = request.POST["comment"]
    recipe = get_object_or_404(Recipe, slug=slug)
    review = Review.objects.create(recipe=recipe, user=request.user, rating=rating, comment=comment)
    
    return JsonResponse({
        "success": True,
        "review": {
            "username": review.user.username,
            "rating": review.rating,
            "comment": review.comment,
        }
    })

@login_required
def view_favorites(request):
    favorites = request.user.favorites.all()
    return render(request, 'recipes/favorites.html', {'favorites': favorites}) 


# Categories
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'recipes/categories.html', {'categories': categories})

def view_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category)
    return render(request, "recipes/view_category.html", {"category": category, "recipes": recipes})

# Popular Recipes
def popular_recipes(request):
    popular = Recipe.objects.order_by("-likes")[:10]
    return render(request, "recipes/popular.html", {"popular": popular})

def search_recipes(request):
    query = request.GET.get("q")
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.none()
    
    return render(request, "search_results.html", {"recipes": recipes, "query": query})

# Custom 404 Page
def custom_404(request, exception):
    return render(request, "404.html", status=404)

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user).select_related('author')
    liked_recipes = user.liked_recipes.all().select_related('author') 

    return render(request, 'recipes/profile.html', {
        'profile_user': user,
        'recipes': recipes,
        'liked_recipes': liked_recipes
    })
    
def search_recipes(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(ingredients__icontains=query) |
            models.Q(tags__name__icontains=query)
        ).distinct()
    else:
        recipes = Recipe.objects.none()
    
    return render(request, 'search_results.html', {'recipes': recipes, 'query': query})

@login_required
def manage_account(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user_profile)

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('manage_account')
    else:
        form = ProfilePictureForm(instance=user_profile)
    
    return render(request, 'manage_account.html', {'form': form, 'user_profile': user_profile})

def recipes(request):
    # Fetch all recipes (or filter as needed)
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/recipes.html', context)

def view_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category)  
    return render(request, "recipes/view_category.html", {"category": category, "recipes": recipes})
