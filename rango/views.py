from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import login_required
from .models import Recipe

# Create your views here.

def home(request):
    """View for the home page displaying all recipes."""
    recipes = Recipe.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes})

def recipe_detail(request):
    """View for the details of a single recipe."""
    recipe = get_object_or_404(Recipe, pk=request.GET.get('recipe_id'))
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    """View for adding a new recipe."""
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')

        if name and description and ingredients and instructions:
            Recipe.objects.create(
                name=name,
                description=description,
                ingredients=ingredients,
                instructions=instructions,
                user=request.user
            )
            return redirect('rango:home')

    return render(request, 'rango/add_recipe.html')

@login_required
def favorites(request):
    """View for displaying a user's favorite recipes."""
    user_favorites = request.user.favorites.all()
    return render(request, 'rango/favorites.html', {'favorites': user_favorites})

def popular_recipes(request):
    """View for displaying the most liked recipes."""
    popular = Recipe.objects.order_by('-likes')[:10]
    return render(request, 'rango/popular.html', {'recipes': popular})
    