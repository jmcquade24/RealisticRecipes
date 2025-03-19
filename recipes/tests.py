import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .models import Recipe, Category, UserProfile, Review, Feedback  
from .forms import RecipeForm, UserProfileForm  
from django.urls import reverse
import time
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.

# TEST MODELS
class RecipeModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Dessert")
        self.recipe = Recipe.objects.create(
            title="Chocolate Cake",
            description="Delicious chocolate cake",
            ingredients="Flour, Sugar, Cocoa, Eggs, Butter",
            instructions="Mix and bake",
            prep_time=30,
            cook_time=45,
            servings=4,
            category=self.category
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, "Chocolate Cake")
        self.assertEqual(self.recipe.category.name, "Dessert")

    def test_recipe_string_representation(self):
        self.assertEqual(str(self.recipe), "Chocolate Cake")

class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = UserProfile.objects.create(user=self.user, bio="Food lover")

    def test_userprofile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.bio, "Food lover")


# TEST FORMS
class RecipeFormTestCase(TestCase):
    def test_valid_recipe_form(self):
        category = Category.objects.create(name="Main Course")
        form_data = {
            "title": "Pasta Alfredo",
            "description": "Creamy pasta with Alfredo sauce",
            "ingredients": "Pasta, Cream, Cheese, Chicken",
            "instructions": "Cook and mix ingredients",
            "prep_time": 20,
            "cook_time": 25,
            "servings": 2,
            "category": category.id
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_form(self):
        form_data = {"title": ""}  # Missing required fields
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())


# TEST VIEWS (INTEGRATION TESTING)
class RecipeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Snacks")
        self.recipe = Recipe.objects.create(
            title="French Fries",
            description="Crispy potato fries",
            ingredients="Potatoes, Oil, Salt",
            instructions="Fry until golden brown",
            prep_time=10,
            cook_time=15,
            servings=2,
            category=self.category,
            author=self.user
        )

    def test_homepage_access(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_view(self):
        response = self.client.get(reverse("recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        response = self.client.get(reverse("recipe_detail", args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)

    def test_login_required_for_dashboard(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_logged_in_user_can_access_dashboard(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)


# TEST API ENDPOINTS
class RecipeAPITestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Drinks")
        self.recipe = Recipe.objects.create(
            title="Lemonade",
            description="Refreshing drink",
            ingredients="Lemon, Sugar, Water",
            instructions="Mix ingredients and serve cold",
            prep_time=5,
            cook_time=0,
            servings=1,
            category=self.category,
            author=self.user
        )

    def test_api_get_request(self):
        response = self.client.get("/api/recipes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_post_request(self):
        data = {
            "title": "Iced Coffee",
            "description": "Cold brewed coffee",
            "ingredients": "Coffee, Ice, Milk, Sugar",
            "instructions": "Brew coffee and serve over ice",
            "prep_time": 10,
            "cook_time": 0,
            "servings": 1,
            "category": self.category.id,
            "author": self.user.id
        }
        response = self.client.post("/api/recipes/", data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_pagination(self):
        response = self.client.get("/api/recipes/?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
