from django.test import TestCase
from django.contrib.auth.models import User
from .models import YourModel 

# Create your tests here.

class YourModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_model_creation(self):
        """Test if the model can be created successfully"""
        obj = YourModel.objects.create(field1="Test", field2=42)
        self.assertEqual(str(obj), "Test")  # Replace with actual __str__ behavior

class AuthenticationTestCase(TestCase):
    def test_login(self):
        """Test user login functionality"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get("/your-protected-url/")  # Replace with actual URL
        self.assertEqual(response.status_code, 200)  # Check if login works

class ViewTestCase(TestCase):
    def test_homepage(self):
        """Test homepage view"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)  # Ensure homepage loads
