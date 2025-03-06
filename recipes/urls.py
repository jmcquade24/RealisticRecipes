from django.urls import path
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'), 
    path('register/', views.register, name='register'),  
    path('login/', views.user_login, name='login'),  
    path('logout/', views.user_logout, name='logout'), 
]
