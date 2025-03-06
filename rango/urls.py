from django.urls import path
from . import views

app_name = 'rango'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('favorites/', views.favorites, name='favorites'),
    path('popular/', views.popular_recipes, name='popular_recipes'),
]
