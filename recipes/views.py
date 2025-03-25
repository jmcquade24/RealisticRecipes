from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from django.db.models import Q

from algoliasearch_django import register
from algoliasearch_django import save_record
from recipes.models import Recipe
from recipes.index import RecipeIndex

from .forms import RecipeForm, UserUpdateForm, UserProfileForm, FeedbackForm, ProfilePictureForm
from .models import Recipe, Review, Category, Like, UserProfile

# Home page
def index(request):
    categories = Category.objects.all()
    featured_recipes = Recipe.objects.filter(is_featured=True)[:3]
    top_categories = Category.objects.all()[:3]
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
<<<<<<< HEAD
        username = request.POST["username"]
        password = request.POST["password"]
        User.objects.create_user(username=username, password=password)
        return redirect("recipes:login")
    return render(request, "recipes/register.html")
=======
        username = request.POST.get("username")
        email = request.POST.get("email") 
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Choose another one.")
            return redirect('recipes:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Try logging in.")
            return redirect('recipes:register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('recipes:login')


    form = UserCreationForm()

    return render(request, 'recipes/register.html', {'form': form})
>>>>>>> 445d1aa725bff36d6dff69f435698190d91c5bc2

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("recipes:index")
        return render(request, "recipes/login.html", {"error": "Invalid credentials"})
    return render(request, "recipes/login.html")

@login_required
def user_logout(request):
    logout(request)
    return redirect("recipes:index")

@login_required
def manage_account(request, username=None):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and profile_picture_form.is_valid():
            form.save()
            profile_picture_form.save()
            return redirect('recipes:user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=user_profile)
        profile_picture_form = ProfilePictureForm(instance=user_profile)
    return render(request, 'recipes/manage_account.html', {
        'form': form,
        'profile_picture_form': profile_picture_form,
        'user_profile': user_profile
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("recipes:index")
    return render(request, "recipes/profile.html")

# Recipe Management
@login_required
def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            save_record(recipe)
            return redirect("recipes:view_recipe", slug=recipe.slug)
    else:
        form = RecipeForm()
    return render(request, "recipes/create_recipe.html", {"form": form})

def view_recipe(request, slug):
    recipe = get_object_or_404(Recipe.objects.select_related('author'), slug=slug)
    reviews = Review.objects.filter(recipe=recipe).select_related('user')
    return render(request, "recipes/view_recipe.html", {"recipe": recipe, "reviews": reviews})

@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.user != recipe.author:
        return redirect('recipes:view_recipe', slug=slug)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect("recipes:view_recipe", slug=recipe.slug)
    return render(request, "recipes/edit_recipe.html", {"form": form, "recipe": recipe})

@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author == request.user:
        recipe.delete()
        return redirect("recipes:index")
    return redirect("recipes:view_recipe", slug=recipe.slug)

# Recipe Interactions
@csrf_exempt
@login_required
@require_POST
def like_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
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

@login_required
def feedback(request):
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
    return render(request, 'recipes/feedback.html', {'form': form})

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

def recipes(request):
    recipes = Recipe.objects.all()
<<<<<<< HEAD
    return render(request, 'recipes/recipes.html', {'recipes': recipes})
=======
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/recipes.html', context)

def view_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category)  
    return render(request, "recipes/view_category.html", {"category": category, "recipes": recipes})

def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Process the password reset
            email = form.cleaned_data["email"]
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    # Generate password reset token and email it to the user
                    # Password reset link will automatically go to password_reset_done
                    pass
            return redirect('password_reset_done') 
    else:
        form = PasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})
>>>>>>> 445d1aa725bff36d6dff69f435698190d91c5bc2
