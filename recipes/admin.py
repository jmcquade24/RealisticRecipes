from django.contrib import admin
from recipes.models import User, UserProfile, Recipe, Review, Category, Like

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Like)
