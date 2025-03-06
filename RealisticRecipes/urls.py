"""RealisticRecipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rango/', include('rango.urls')),
    path('admin/', admin.site.urls),
    path('', include('rango.urls')),

    # User Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),

    # Recipes
    path('recipes/create/', views.create_recipe, name='create_recipe'),
    path('recipes/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('recipes/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),

    # Categories
    path('categories/', views.view_categories, name='view_categories'),

    # User Interactions
    path('recipes/<int:recipe_id>/like/', views.like_recipe, name='like_recipe'),
    path('recipes/<int:recipe_id>/favorite/', views.favorite_recipe, name='favorite_recipe'),
    path('recipes/<int:recipe_id>/review/', views.add_review, name='add_review'),
    path('favorites/', views.view_favorites, name='view_favorites'),

    # Popular Page
    path('popular/', views.popular_recipes, name='popular_recipes'),
]
