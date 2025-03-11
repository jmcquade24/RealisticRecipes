from django import forms
from .models import Recipe, Category, UserProfile

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 
                  'instructions', 'prep_time', 'cook_time', 
                  'servings', 'image', 'category']
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']