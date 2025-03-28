from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
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

    #forgotten password     
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Recipe Management
    path("recipes/", views.recipes, name="recipes"),
    path("create/", views.create_recipe, name="create_recipe"),
    path("recipe/<slug:slug>/", views.view_recipe, name="view_recipe"),
    path("recipe/<slug:slug>/delete/", views.delete_recipe, name="delete_recipe"),
    path("recipe/<slug:slug>/edit/", views.edit_recipe, name="edit_recipe"),

    # Interactions
    path("recipe/<slug:slug>/like/", views.like_recipe, name="like_recipe"),
    path("recipe/<slug:slug>/favorite/", views.favorite_recipe, name="favorite_recipe"),
    path("recipe/<slug:slug>/review/", views.add_review, name="add_review"),
    path("add-review/", views.add_review, name="add_review"),

    # Categories
    path("categories/", views.view_categories, name="view_categories"),
    path("category/<int:category_id>/", views.view_category, name="view_category"),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/pending/', views.pending_categories, name='pending_categories'),
    path('categories/<int:pk>/approve/', views.approve_category, name='approve_category'),

    
    # Popular & Search
    path("popular/", views.popular_recipes, name="popular_recipes"),
    path("search/", views.search_recipes, name="search"),

    #feedback  
    path('feedback/', views.feedback, name='feedback'),

    # User Profiles
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("profile/<str:username>/manage-profile/", views.manage_account, name="manage_account"),

        # Authentication
    path("accounts/signup/", views.register, name="signup"),
    path("accounts/login/", views.user_login, name="login"),
    path("accounts/logout/", views.user_logout, name="logout"),
    path("accounts/delete/", views.delete_account, name="delete_account"),

    # Password Management
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


# Serving media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
