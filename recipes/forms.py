from django import forms
from .models import Recipe, Category, UserProfile, User, Review

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
        
class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Review
        fields = ['rating', 'comment']