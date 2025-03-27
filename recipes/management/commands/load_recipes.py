from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from algolia_search.algolia_config import client
from RealisticRecipes import settings
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Loads 30+ demo recipes with categories'

    def handle(self, *args, **options):

        # Create categories if they don't exist
        categories = {
            "Korean": self.get_or_create_category("Korean"),
            "Mongolian": self.get_or_create_category("Mongolian"),
            "Chinese": self.get_or_create_category("Chinese"),
            "Indian": self.get_or_create_category("Indian"),
            "Vegan": self.get_or_create_category("Vegan"),
            "Vegetarian": self.get_or_create_category("Vegetarian"),
            "Quick Cook": self.get_or_create_category("Quick Cook"),
            "Gluten Free": self.get_or_create_category("Gluten Free"),
            "Breakfast": self.get_or_create_category("Breakfast"),
            "Lunch": self.get_or_create_category("Lunch"),
            "Dinner": self.get_or_create_category("Dinner"),
            "Family Friendly": self.get_or_create_category("Family Friendly"),
            "Home Alone": self.get_or_create_category("Home Alone"),
            "Comfort Food": self.get_or_create_category("Comfort Food"),
            "Desserts": self.get_or_create_category("Desserts")
        }
        
        # Get or create admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpass'
            )
        
        recipes_data = [
            # Korean
            {
                "title": "Kimchi Fried Rice",
                "description": "Spicy fermented cabbage fried with rice",
                "ingredients": "Kimchi, Rice, Gochujang, Egg, Green Onions",
                "instructions": "1. Fry kimchi\n2. Add rice\n3. Top with fried egg",
                "prep_time": 10,
                "cook_time": 10,
                "servings": 2,
                "category": categories["Korean"]
            },
            {
                "title": "Bibimbap",
                "description": "Korean mixed rice bowl",
                "ingredients": "Rice, Vegetables, Beef, Egg, Gochujang",
                "instructions": "1. Arrange ingredients on rice\n2. Mix with sauce",
                "prep_time": 20,
                "cook_time": 10,
                "servings": 2,
                "category": categories["Korean"]
            },
            
            # Mongolian
            {
                "title": "Mongolian Beef",
                "description": "Sweet and savory stir-fried beef",
                "ingredients": "Beef, Soy Sauce, Brown Sugar, Garlic, Ginger",
                "instructions": "1. Marinate beef\n2. Stir-fry with sauce",
                "prep_time": 15,
                "cook_time": 10,
                "servings": 4,
                "category": categories["Mongolian"]
            },
            
            # Chinese
            {
                "title": "Kung Pao Chicken",
                "description": "Spicy stir-fry with peanuts",
                "ingredients": "Chicken, Peanuts, Chili, Soy Sauce",
                "instructions": "1. Stir-fry chicken\n2. Add sauce and peanuts",
                "prep_time": 15,
                "cook_time": 10,
                "servings": 3,
                "category": categories["Chinese"]
            },
            {
                "title": "Dumplings",
                "description": "Steamed or fried filled dough pockets",
                "ingredients": "Flour, Pork, Cabbage, Ginger",
                "instructions": "1. Make filling\n2. Wrap in dough\n3. Cook",
                "prep_time": 30,
                "cook_time": 10,
                "servings": 4,
                "category": categories["Chinese"]
            },
            
            # Indian
            {
                "title": "Butter Chicken",
                "description": "Creamy tomato-based curry",
                "ingredients": "Chicken, Tomatoes, Cream, Spices",
                "instructions": "1. Marinate chicken\n2. Cook in sauce",
                "prep_time": 20,
                "cook_time": 30,
                "servings": 4,
                "category": categories["Indian"]
            },
            {
                "title": "Chana Masala",
                "description": "Spicy chickpea curry",
                "ingredients": "Chickpeas, Tomatoes, Onions, Spices",
                "instructions": "1. Sauté onions\n2. Add spices and chickpeas",
                "prep_time": 10,
                "cook_time": 25,
                "servings": 3,
                "category": categories["Indian"]
            },
            
            # Vegan
            {
                "title": "Vegan Buddha Bowl",
                "description": "Nutritious plant-based bowl",
                "ingredients": "Quinoa, Sweet Potato, Avocado, Chickpeas",
                "instructions": "1. Roast veggies\n2. Assemble bowl",
                "prep_time": 15,
                "cook_time": 20,
                "servings": 1,
                "category": categories["Vegan"]
            },
            
            # Vegetarian
            {
                "title": "Caprese Salad",
                "description": "Simple Italian salad",
                "ingredients": "Tomatoes, Mozzarella, Basil, Olive Oil",
                "instructions": "1. Slice ingredients\n2. Arrange and drizzle",
                "prep_time": 10,
                "cook_time": 0,
                "servings": 2,
                "category": categories["Vegetarian"]
            },
            
            # Quick Cook
            {
                "title": "Avocado Toast",
                "description": "Simple breakfast toast",
                "ingredients": "Bread, Avocado, Salt, Pepper",
                "instructions": "1. Toast bread\n2. Mash avocado on top",
                "prep_time": 5,
                "cook_time": 2,
                "servings": 1,
                "category": categories["Quick Cook"]
            },
            
            # Gluten Free
            {
                "title": "Quinoa Salad",
                "description": "Healthy gluten-free salad",
                "ingredients": "Quinoa, Cucumber, Cherry Tomatoes, Lemon",
                "instructions": "1. Cook quinoa\n2. Mix with veggies",
                "prep_time": 10,
                "cook_time": 15,
                "servings": 2,
                "category": categories["Gluten Free"]
            },
            
            # Breakfast
            {
                "title": "Pancakes",
                "description": "Fluffy breakfast pancakes",
                "ingredients": "Flour, Milk, Eggs, Baking Powder",
                "instructions": "1. Mix batter\n2. Cook on griddle",
                "prep_time": 10,
                "cook_time": 15,
                "servings": 4,
                "category": categories["Breakfast"]
            },
            
            # Lunch
            {
                "title": "Chicken Wrap",
                "description": "Easy lunch wrap",
                "ingredients": "Tortilla, Chicken, Lettuce, Mayo",
                "instructions": "1. Fill tortilla\n2. Roll up",
                "prep_time": 5,
                "cook_time": 0,
                "servings": 1,
                "category": categories["Lunch"]
            },
            
            # Dinner
            {
                "title": "Beef Stew",
                "description": "Hearty dinner stew",
                "ingredients": "Beef, Potatoes, Carrots, Onions",
                "instructions": "1. Brown beef\n2. Simmer with veggies",
                "prep_time": 20,
                "cook_time": 120,
                "servings": 6,
                "category": categories["Dinner"]
            },
            
            # Family Friendly
            {
                "title": "Mac & Cheese",
                "description": "Classic kid-friendly dish",
                "ingredients": "Pasta, Cheese, Milk, Butter",
                "instructions": "1. Cook pasta\n2. Make cheese sauce",
                "prep_time": 10,
                "cook_time": 15,
                "servings": 4,
                "category": categories["Family Friendly"]
            },
            
            # Home Alone
            {
                "title": "Microwave Mug Cake",
                "description": "Single-serving dessert",
                "ingredients": "Flour, Sugar, Cocoa, Milk",
                "instructions": "1. Mix in mug\n2. Microwave 1 minute",
                "prep_time": 2,
                "cook_time": 1,
                "servings": 1,
                "category": categories["Home Alone"]
            },
            
            # Comfort Food
            {
                "title": "Mashed Potatoes",
                "description": "Creamy comfort side dish",
                "ingredients": "Potatoes, Butter, Milk, Salt",
                "instructions": "1. Boil potatoes\n2. Mash with butter",
                "prep_time": 10,
                "cook_time": 20,
                "servings": 4,
                "category": categories["Comfort Food"]
            },
            
            # Desserts
            {
                "title": "Chocolate Chip Cookies",
                "description": "Classic homemade cookies",
                "ingredients": "Flour, Butter, Sugar, Chocolate Chips",
                "instructions": "1. Mix dough\n2. Bake at 350°F for 10 mins",
                "prep_time": 15,
                "cook_time": 10,
                "servings": 24,
                "category": categories["Desserts"]
            }
        ]

        def serialise_recipe(recipe):
            return {
            "objectID": recipe.slug,
            "title": recipe.title,
            "description": recipe.description,
            "slug": recipe.slug,
            }
        
        async def save_and_wait(recipe):
            check_if_present = client.search("search_query", {"filters": f"title:'{recipe.title}'"})
            if check_if_present["nbHits"] == 0:
                response = await client.save_object("recipes", serialise_recipe(recipe))
                await client.wait_for_task(index_name="recipes", task_id=response["taskID"])

        # Create recipes
        for recipe_data in recipes_data:
            recipe = Recipe.objects.create(
                **recipe_data,
                author=admin_user
            )
            recipe.slug = slugify(recipe.title) + "-" + recipe.author.get_username()
            save_and_wait(recipe)
            
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(recipes_data)} recipes across {len(categories)} categories!'))

    def get_or_create_category(self, name):
        category, created = Category.objects.get_or_create(name=name)
        if created:
            self.stdout.write(f'Created category: {name}')
        return category
    
    