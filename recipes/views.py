from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Recipe, Review, Category, Like
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    return render(request, 'recipes/index.html')

def home(request):
    return render(request, 'recipes/home.html')

def about(request):
    return render(request, 'recipes/about.html')
    
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            return render(request, 'recipes/register.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'recipes/register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'recipes/login.html', {'error': 'Invalid credentials'})
    return render(request, 'recipes/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def delete_account(request):
    if not request.user.is_authenticated:
        return redirect('recipes:login')  
    request.user.delete()
    return redirect('index')

@login_required
def create_recipe(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']

        if not title or not description:
            return render(request, 'recipes/create_recipe.html', {'categories': Category.objects.all(), 'error': 'Title and description are required'})

        try:
            category = Category.objects.get(id=request.POST['category'])
        except Category.DoesNotExist:
            return render(request, 'recipes/create_recipe.html', {'categories': Category.objects.all(), 'error': 'Invalid category selected'})  
        
        recipe = Recipe.objects.create(title=title, description=description, category=category, author=request.user)   
        return redirect('recipes:view_recipe', recipe_id=recipe.id) 
    categories = Category.objects.all()
    return render(request, 'recipes/create_recipe.html', {'categories': categories})

@login_required
def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = Review.objects.filter(recipe=recipe)
    return render(request, 'recipes/view_recipe.html', {'recipe': recipe, 'reviews': reviews})

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return HttpResponse("You are not allowed to delete this recipe.", status=403)
    recipe.delete()
    return redirect('index')

def view_categories(request):
    categories = Category.objects.filter(recipe__isnull=False).distinct()
    return render(request, 'recipes/categories.html', {'categories': categories})


@require_POST
@login_required
def like_recipe(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user in recipe.likes.all():
            recipe.likes.remove(request.user)
            liked = False
        else:
            recipe.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': recipe.likes.count()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def favorite_recipe(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user in recipe.favorites.all():
            recipe.favorites.remove(request.user)
        else:
            recipe.favorites.add(request.user)
        return redirect('recipes:view_favorites')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def view_favorites(request):
    favorites = request.user.favorites.all()
    return render(request, 'recipes/favorites.html', {'favorites': favorites}) 

@login_required
def add_review(request, recipe_id):
    if request.method == "POST":
        rating = request.POST['rating']
        comment = request.POST['comment']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Review.objects.create(recipe=recipe, user=request.user, rating=rating, comment=comment)
    return redirect('recipes:view_recipe', recipe_id=recipe_id)

def popular_recipes(request):
    popular = Recipe.objects.order_by('-likes')[:10]
    return render(request, 'recipes/popular.html', {'popular': popular})

def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def popular_recipes(request):
    popular = Recipe.objects.order_by('-likes')[-10]
    return render(request, 'popular.html', {'popular' : popular})

def homepage(request):
    featured_recipes = Recipe.objects.filter(is_featured=True)[:3]  # Get the top 3 featured recipes
    top_categories = Category.objects.all()[:3]  # Get the top 3 categories
    return render(request, 'homepage.html', {
        'featured_recipes': featured_recipes,
        'top_categories': top_categories
    })
