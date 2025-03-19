import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .models import Recipe, Category, UserProfile 
from .forms import RecipeForm, UserProfileForm

# Create your tests here.

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

# Unit Test for Forms
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

# Integration Test for Views
class RecipeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
    
    def test_view_requires_login(self):
        response = self.client.get("/recipes/")  # Adjust to actual view URL
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_view_after_login(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)

# API Test
class RecipeAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
    
    def test_api_get_request(self):
        response = self.client.get("/api/recipes/")  # Adjust API endpoint
        self.assertEqual(response.status_code, 200)
    
    def test_api_post_request(self):
        response = self.client.post("/api/recipes/", {"title": "Test Recipe"}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

# UI Test using Selenium
class UITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()  # Ensure chromedriver is installed
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
    def test_login_page(self):
        self.driver.get("http://127.0.0.1:8000/login/")  # Adjust to actual login URL
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.NAME, "submit")
        
        username_field.send_keys("testuser")
        password_field.send_keys("testpass")
        submit_button.click()
        
        self.assertIn("Dashboard", self.driver.title)  # Adjust this based on expected page title after login

if __name__ == "__main__":
    unittest.main()
