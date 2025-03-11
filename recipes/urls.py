from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'), 
    path('register/', views.register, name='register'),  
    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'), 

    # Recipe management
    path('recipes/', views.recipes, name='recipes'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),

    # Categories & Interactions
    path('categories/', views.view_categories, name='view_categories'),
    path('<int:recipe_id>/like/', views.like_recipe, name='like_recipe'),
    path('<int:recipe_id>/favorite/', views.favorite_recipe, name='favorite_recipe'),
    path('<int:recipe_id>/review/', views.add_review, name='add_review'),
    path('favorites/', views.view_favorites, name='view_favorites'),

    # Popular recipes
    path('popular/', views.popular_recipes, name='popular_recipes'),
]
