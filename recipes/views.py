from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Recipe, Review, Category, Like
from django.contrib.auth.models import User

# Home page
def index(request):
    return render(request, "recipes/index.html")

def home(request):
    return render(request, 'recipes/home.html')


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
    return redirect("index")

@login_required
def delete_account(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")  
    
    request.user.delete()
    return redirect("index")

# Recipe Management
@login_required
def create_recipe(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]

        if not title or not description:
            return render(request, "recipes/create_recipe.html", {"categories": Category.objects.all(), "error": "Title and description are required"})

        try:
            category = Category.objects.get(id=request.POST["category"])
        except Category.DoesNotExist:
            return render(request, "recipes/create_recipe.html", {"categories": Category.objects.all(), "error": "Invalid category selected"})

        recipe = Recipe.objects.create(title=title, description=description, category=category, author=request.user)
        return redirect("recipes:view_recipe", slug=recipe.slug)

    categories = Category.objects.all()
    return render(request, "recipes/create_recipe.html", {"categories": categories})

def view_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, "recipes/view_recipe.html", {"recipe": recipe})

@login_required
def delete_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.author == request.user:  # Ensuring only the creator can delete
        recipe.delete()
        return redirect("recipes:index")
    return redirect("recipes:view_recipe", slug=slug)

# Recipe Interactions
@login_required
@require_POST
def like_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    recipe.likes += 1
    recipe.save()
    return JsonResponse({"success": True, "likes": recipe.likes})

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
    Review.objects.create(recipe=recipe, user=request.user, rating=rating, comment=comment)
    return redirect("recipes:view_recipe", slug=slug)

@login_required
def view_favorites(request):
    favorites = request.user.favorites.all()
    return render(request, 'recipes/favorites.html', {'favorites': favorites}) 


# Categories
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'recipes/categories.html', {'categories': categories})

# Popular Recipes
def popular_recipes(request):
    popular = Recipe.objects.order_by("-likes")[:10]
    return render(request, "recipes/popular.html", {"popular": popular})

# Custom 404 Page
def custom_404(request, exception):
    return render(request, "404.html", status=404)


def homepage(request):
    featured_recipes = Recipe.objects.filter(is_featured=True)[:3]  # Get the top 3 featured recipes
    top_categories = Category.objects.all()[:3]  # Get the top 3 categories
    return render(request, 'recipes/home.html', {
        'featured_recipes': featured_recipes,
        'top_categories': top_categories
    })


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('home')
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('view_recipe', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'edit_recipe.html', {'form': form})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user)
    liked_recipes = user.liked_recipes.all()
    return render(request, 'user_profile.html', {
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
    
    return render(request, 'manage_account.html', {'form': form})
