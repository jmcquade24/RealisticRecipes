from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'), 

    path("create/", views.create_recipe, name="create_recipe"),
    path("recipe/<slug:slug>/", views.view_recipe, name="view_recipe"), 
    path("recipe/<slug:slug>/delete/", views.delete_recipe, name="delete_recipe"),

    path("categories/", views.view_categories, name="view_categories"),
    path("recipe/<slug:slug>/like/", views.like_recipe, name="like_recipe"),  # Uses AJAX
    path("recipe/<slug:slug>/favorite/", views.favorite_recipe, name="favorite_recipe"),
    path("recipe/<slug:slug>/review/", views.add_review, name="add_review"),
    path("favorites/", views.view_favorites, name="view_favorites"),

    path('popular/', views.popular_recipes, name='popular_recipes'),
]
