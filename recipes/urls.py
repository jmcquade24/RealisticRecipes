from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Use relative import for better modularity

app_name = "recipes"

urlpatterns = [
    # Core pages
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),

    # Authentication
    path("register", views.register, name="register"),  
    path("login/", views.user_login, name="login"),  
    path("logout/", views.user_logout, name="logout"), 

    # Recipe Management
    path("recipes/", views.recipes, name="recipes"),
    path("create/", views.create_recipe, name="create_recipe"),
    path("recipe/<slug:slug>/", views.view_recipe, name="view_recipe"),
    path("recipe/<slug:slug>/delete/", views.delete_recipe, name="delete_recipe"),
    path('recipe/<slug:slug>/edit/', views.edit_recipe, name='edit_recipe'),

    # Categories & Interactions
    path("categories/", views.view_categories, name="view_categories"),
    path("category/<int:category_id>/", views.view_category, name="view_category"),
    path("recipe/<slug:slug>/like/", views.like_recipe, name="like_recipe"),  # Uses AJAX
    path("recipe/<slug:slug>/favorite/", views.favorite_recipe, name="favorite_recipe"),
    path("recipe/<slug:slug>/review/", views.add_review, name="add_review"),
    path('add-review/', views.add_review, name='add_review'),
    path("favorites/", views.view_favorites, name="view_favorites"),

    # Popular & Search
    path("popular/", views.popular_recipes, name="popular_recipes"),
    path("search/", views.search_recipes, name="search_recipes"),

    # User Profiles
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path('profile/<str:username>/manage-profile/', views.manage_account, name='manage_account'),

    # Feedback
    path("feedback/", views.feedback_view, name="feedback"),

]

# Serving media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
