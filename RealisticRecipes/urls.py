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
from recipes import views
from django.conf.urls.static import static
from django.conf import settings
from recipes.views import profile_view, manage_account_view, delete_account_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Core routes
    path('', views.index, name='index'),
    path('recipes/', include('recipes.urls')),
    path('admin/', admin.site.urls),

    # Authentication
    path('recipes/', include('recipes.urls')),
    path("accounts/signup/", views.register, name="signup"), 
    path("accounts/login/", views.user_login, name="login"),
    path("accounts/logout/", views.user_logout, name="logout"),
    path("accounts/delete/", views.delete_account, name="delete_account"),

    # User Account Management
    path("manage-account/", manage_account_view, name="manage_account"),
    path("profile/", profile_view, name="profile"),

    # Password Management
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done') 

]

# Custom 404 Handler
handler404 = "recipes.views.custom_404"

# Serving media and static files in developmen
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
