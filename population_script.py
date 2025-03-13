import os
import django
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RealisticRecipes.settings")
django.setup()

from recipes.models import UserProfile, Category, Recipe, Review, Like, User

# Create users
users = [
    {
        "username": "JamieAtHome",
        "email": "jamie@cooking.com",
        "bio": "Home cook passionate about Mediterranean flavors",
    },
    {
        "username": "SophieSpice",
        "email": "sophie@spiceitup.com",
        "bio": "Spice enthusiast exploring global cuisines",
    },
    {
        "username": "MarcusMeals",
        "email": "marcus@quickmeals.com",
        "bio": "Specializing in quick, nutritious weeknight dinners",
    },
]

# Create categories
categories = [
    {"name": "Breakfast"},
    {"name": "Main Course"},
    {"name": "Dessert"},
    {"name": "Appetizer"},
    {"name": "Soup"},
]

# Create recipes
recipes = [
    {
        "user_index": 0,
        "title": "Lemon Ricotta Pancakes",
        "description": "Light and fluffy pancakes with a hint of lemon and creamy ricotta cheese.",
        "ingredients": "- 1 1/2 cups all-purpose flour\n- 3 tablespoons sugar\n- 2 teaspoons baking powder\n- 1/2 teaspoon baking soda\n- 1/2 teaspoon salt\n- 1 cup ricotta cheese\n- 3/4 cup milk\n- 3 large eggs, separated\n- 1 tablespoon lemon zest\n- 2 tablespoons lemon juice\n- 1 teaspoon vanilla extract\n- 2 tablespoons butter, melted",
        "instructions": "1. In a large bowl, whisk together flour, sugar, baking powder, baking soda, and salt.\n2. In a separate bowl, combine ricotta, milk, egg yolks, lemon zest, lemon juice, vanilla, and melted butter.\n3. Add the wet ingredients to the dry ingredients and mix until just combined.\n4. Beat the egg whites until stiff peaks form, then gently fold into the batter.\n5. Heat a griddle or non-stick pan over medium heat and lightly grease.\n6. Pour 1/4 cup of batter for each pancake and cook until bubbles form, about 2-3 minutes.\n7. Flip and cook for another 1-2 minutes until golden brown.\n8. Serve with maple syrup, fresh berries, and a dusting of powdered sugar.",
        "prep_time": 15,
        "cook_time": 20,
        "servings": 4,
        "category_index": 0,
        "image_path": "population_script_images/lemon_ricotta_pancakes.jpg",
    },
    {
        "user_index": 1,
        "title": "Moroccan Spiced Lamb Tagine",
        "description": "A fragrant, slow-cooked Moroccan stew with tender lamb, apricots, and a blend of aromatic spices.",
        "ingredients": "- 2 pounds lamb shoulder, cut into 1.5-inch cubes\n- 2 tablespoons olive oil\n- 2 large onions, chopped\n- 4 garlic cloves, minced\n- 2 tablespoons fresh ginger, grated\n- 2 teaspoons ground cumin\n- 2 teaspoons ground coriander\n- 1 teaspoon ground cinnamon\n- 1 teaspoon paprika\n- 1/2 teaspoon ground turmeric\n- 1/4 teaspoon cayenne pepper\n- 1 can (14.5 oz) diced tomatoes\n- 2 cups chicken broth\n- 1/2 cup dried apricots, chopped\n- 1/4 cup green olives, pitted\n- 2 tablespoons honey\n- 1 lemon, zested and juiced\n- 1/4 cup fresh cilantro, chopped\n- 1/4 cup fresh mint, chopped\n- Salt and pepper to taste",
        "instructions": "1. Season lamb with salt and pepper. Heat olive oil in a large Dutch oven over medium-high heat.\n2. Working in batches, brown the lamb on all sides, about 5 minutes per batch. Transfer to a plate.\n3. Reduce heat to medium and add onions to the pot. Cook until softened, about 5 minutes.\n4. Add garlic and ginger, cook for 1 minute until fragrant.\n5. Stir in all the spices and cook for 30 seconds until fragrant.\n6. Return the lamb to the pot, add tomatoes and broth, bring to a simmer.\n7. Cover and reduce heat to low. Simmer for 1.5 hours until meat is tender.\n8. Add apricots, olives, honey, lemon zest, and juice. Simmer uncovered for 30 minutes until sauce thickens.\n9. Stir in fresh herbs, adjust seasoning, and serve over couscous.",
        "prep_time": 30,
        "cook_time": 120,
        "servings": 6,
        "category_index": 1,
        "image_path": "population_script_images/moroccan_lamb_tagine.jpg",
    },
    {
        "user_index": 2,
        "title": "Dark Chocolate Avocado Mousse",
        "description": "A rich, creamy chocolate dessert with a healthy twist using avocados instead of heavy cream.",
        "ingredients": "- 2 ripe avocados, peeled and pitted\n- 1/2 cup unsweetened cocoa powder\n- 1/2 cup pure maple syrup (or to taste)\n- 1/4 cup almond milk\n- 2 teaspoons vanilla extract\n- 1/4 teaspoon espresso powder (optional)\n- Pinch of salt\n- 1/4 cup dark chocolate chips, melted\n- Fresh berries and mint for garnish",
        "instructions": "1. Place avocados in a food processor and blend until smooth.\n2. Add cocoa powder, maple syrup, almond milk, vanilla, espresso powder (if using), and salt.\n3. Blend until completely smooth, stopping to scrape down the sides as needed.\n4. Add the melted chocolate and blend again until incorporated.\n5. Taste and adjust sweetness if needed.\n6. Transfer to serving glasses or bowls and refrigerate for at least 2 hours to set.\n7. Garnish with fresh berries and mint before serving.",
        "prep_time": 15,
        "cook_time": 0,
        "servings": 4,
        "category_index": 2,
        "image_path": "population_script_images/chocolate_avocado_mousse.jpg",
    },
    {
        "user_index": 0,
        "title": "Crispy Baked Sweet Potato Falafel",
        "description": "A healthier take on traditional falafel using sweet potatoes as the base, baked instead of fried.",
        "ingredients": "- 1 large sweet potato (about 1 pound), roasted and cooled\n- 1 can (15 oz) chickpeas, drained and rinsed\n- 1/4 cup fresh parsley, chopped\n- 1/4 cup fresh cilantro, chopped\n- 3 cloves garlic, minced\n- 1 teaspoon ground cumin\n- 1 teaspoon ground coriander\n- 1/2 teaspoon paprika\n- 1/4 teaspoon cayenne pepper\n- 1 tablespoon lemon juice\n- 1/2 cup chickpea flour (or all-purpose flour)\n- 1 teaspoon baking powder\n- Salt and pepper to taste\n- 2 tablespoons olive oil",
        "instructions": "1. Preheat oven to 425°F (220°C) and line a baking sheet with parchment paper.\n2. In a food processor, combine sweet potato, chickpeas, herbs, and garlic. Pulse until combined but still slightly chunky.\n3. Add spices, lemon juice, flour, baking powder, salt, and pepper. Pulse a few more times until the mixture comes together.\n4. Using a tablespoon or cookie scoop, form the mixture into balls (about 24 total).\n5. Place on the prepared baking sheet, brush with olive oil, and bake for 25-30 minutes, flipping halfway through, until golden and crispy.\n6. Serve warm with tahini sauce, in pita bread with fresh vegetables, or on top of a salad.",
        "prep_time": 20,
        "cook_time": 30,
        "servings": 6,
        "category_index": 3,
        "image_path": "population_script_images/sweet_potato_falafel.jpg",
    },
    {
        "user_index": 1,
        "title": "Roasted Butternut Squash and Apple Soup",
        "description": "A comforting autumn soup blending sweet butternut squash with tart apples and warming spices.",
        "ingredients": "- 1 medium butternut squash (about 2-3 pounds), peeled, seeded, and cubed\n- 2 tart apples (like Granny Smith), peeled, cored, and chopped\n- 1 large onion, chopped\n- 2 carrots, chopped\n- 3 cloves garlic, minced\n- 2 tablespoons olive oil\n- 1 teaspoon ground cinnamon\n- 1/2 teaspoon ground nutmeg\n- 1/4 teaspoon ground cloves\n- 4 cups vegetable broth\n- 1 cup apple cider\n- 1/2 cup heavy cream (optional)\n- Salt and pepper to taste\n- Roasted pumpkin seeds and a drizzle of cream for garnish",
        "instructions": "1. Preheat oven to 400°F (200°C).\n2. On a large baking sheet, toss butternut squash, apples, onion, carrots, and garlic with olive oil, salt, and pepper.\n3. Roast for 30-35 minutes until vegetables are tender and caramelized, stirring halfway through.\n4. Transfer roasted vegetables to a large pot, add spices, vegetable broth, and apple cider.\n5. Bring to a simmer and cook for 10 minutes to allow flavors to meld.\n6. Using an immersion blender (or working in batches with a regular blender), purée the soup until smooth.\n7. Stir in cream if using, and adjust seasoning.\n8. Reheat gently if needed, garnish with roasted pumpkin seeds and a drizzle of cream, and serve.",
        "prep_time": 20,
        "cook_time": 45,
        "servings": 6,
        "category_index": 4,
        "image_path": "population_script_images/butternut_squash_soup.jpg",
    },
]

# Create reviews
reviews = [
    {
        "recipe_index": 0,
        "user_index": 1,
        "rating": 5,
        "comment": "These pancakes are incredibly fluffy and the lemon flavor is perfect. My new weekend breakfast favorite!",
    },
    {
        "recipe_index": 1,
        "user_index": 2,
        "rating": 4,
        "comment": "The spice combination is fantastic. I added a cinnamon stick and a bay leaf while simmering for extra flavor.",
    },
    {
        "recipe_index": 2,
        "user_index": 0,
        "rating": 5,
        "comment": "I was skeptical about avocado in a dessert, but this is amazing! So rich and creamy, you'd never guess it's actually healthy.",
    },
    {
        "recipe_index": 3,
        "user_index": 2,
        "rating": 4,
        "comment": "Great vegetarian option! I added a bit more spice and they were perfect. The sweet potato adds a nice complexity.",
    },
    {
        "recipe_index": 4,
        "user_index": 0,
        "rating": 5,
        "comment": "Perfect fall soup! The apple adds just the right amount of sweetness to balance the squash.",
    },
]

# Create likes
likes = [
    {"recipe_index": 0, "user_index": 1},
    {"recipe_index": 0, "user_index": 2},
    {"recipe_index": 1, "user_index": 0},
    {"recipe_index": 2, "user_index": 0},
    {"recipe_index": 2, "user_index": 1},
    {"recipe_index": 3, "user_index": 2},
    {"recipe_index": 4, "user_index": 0},
    {"recipe_index": 4, "user_index": 2},
]


def add_user(user_dict):
    user_model = User.objects.get_or_create(
        username=user_dict["username"], email=user_dict["email"]
    )[0]
    user_model.set_password("testpassword123")  # Setting a default password
    user_model.save()

    user_profile = UserProfile.objects.get_or_create(
        user=user_model, bio=user_dict["bio"]
    )[0]
    user_profile.save()
    return user_profile


def add_category(category_dict):
    category = Category.objects.get_or_create(name=category_dict["name"])[0]
    category.save()
    return category


def add_recipe(recipe_dict):
    # Try to open the image file, or proceed without it if file doesn't exist
    try:
        with open(recipe_dict["image_path"], "rb") as f:
            recipe = Recipe.objects.get_or_create(
                author=User.objects.all()[recipe_dict["user_index"]],
                title=recipe_dict["title"],
                description=recipe_dict["description"],
                ingredients=recipe_dict["ingredients"],
                instructions=recipe_dict["instructions"],
                prep_time=recipe_dict["prep_time"],
                cook_time=recipe_dict["cook_time"],
                servings=recipe_dict["servings"],
                category=Category.objects.all()[recipe_dict["category_index"]],
                image=File(f, name=os.path.basename(recipe_dict["image_path"])),
            )[0]
    except FileNotFoundError:
        recipe = Recipe.objects.get_or_create(
            author=User.objects.all()[recipe_dict["user_index"]],
            title=recipe_dict["title"],
            description=recipe_dict["description"],
            ingredients=recipe_dict["ingredients"],
            instructions=recipe_dict["instructions"],
            prep_time=recipe_dict["prep_time"],
            cook_time=recipe_dict["cook_time"],
            servings=recipe_dict["servings"],
            category=Category.objects.all()[recipe_dict["category_index"]],
        )[0]

    recipe.save()
    return recipe


def add_review(review_dict):
    review = Review.objects.get_or_create(
        recipe=Recipe.objects.all()[review_dict["recipe_index"]],
        user=User.objects.all()[review_dict["user_index"]],
        rating=review_dict["rating"],
        comment=review_dict["comment"],
    )[0]
    review.save()
    return review


def add_like(like_dict):
    # Add a direct like record
    like = Like.objects.get_or_create(
        recipe=Recipe.objects.all()[like_dict["recipe_index"]],
        user=User.objects.all()[like_dict["user_index"]],
    )[0]
    like.save()

    # Also add to the ManyToMany field in Recipe model
    recipe = Recipe.objects.all()[like_dict["recipe_index"]]
    user = User.objects.all()[like_dict["user_index"]]
    recipe.likes.add(user)

    return like


def add_users(users_dict):
    try:
        for user_dict in users_dict:
            add_user(user_dict)

        jamie = User.objects.get(username="JamieAtHome")
        assert (
            jamie.userprofile.bio == "Home cook passionate about Mediterranean flavors"
        )
        print("- Users added successfully ✔")
        return True
    except Exception as e:
        error_message = f"Error adding users: {e}"
        print(error_message)
        return False


def add_categories(categories_dict):
    try:
        for category_dict in categories_dict:
            add_category(category_dict)

        breakfast = Category.objects.get(name="Breakfast")
        assert breakfast.name == "Breakfast"
        print("- Categories added successfully ✔")
        return True
    except Exception as e:
        error_message = f"Error adding categories: {e}"
        print(error_message)
        return False


def add_recipes(recipes_dict):
    try:
        for recipe_dict in recipes_dict:
            add_recipe(recipe_dict)

        tagine = Recipe.objects.get(title="Moroccan Spiced Lamb Tagine")
        assert tagine.author.username == "SophieSpice"
        print("- Recipes added successfully ✔")
        return True
    except Exception as e:
        error_message = f"Error adding recipes: {e}"
        print(error_message)
        return False


def add_reviews(reviews_dict):
    try:
        for review_dict in reviews_dict:
            add_review(review_dict)

        first_review = Review.objects.get(comment__contains="incredibly fluffy")
        assert first_review.rating == 5
        print("- Reviews added successfully ✔")
        return True
    except Exception as e:
        error_message = f"Error adding reviews: {e}"
        print(error_message)
        return False


def add_likes(likes_dict):
    try:
        for like_dict in likes_dict:
            add_like(like_dict)

        # Verify likes were added correctly
        first_recipe = Recipe.objects.all()[0]
        assert first_recipe.likes.count() == 2
        print("- Likes added successfully ✔")
        return True
    except Exception as e:
        error_message = f"Error adding likes: {e}"
        print(error_message)
        return False


def add_favorites():
    try:
        # Add some sample favorites
        recipes = Recipe.objects.all()
        users = User.objects.all()

        # First user favorites first and third recipe
        recipes[0].favorites.add(users[0])
        recipes[2].favorites.add(users[0])

        # Second user favorites second and fifth recipe
        recipes[1].favorites.add(users[1])
        recipes[4].favorites.add(users[1])

        # Third user favorites third and fourth recipe
        recipes[2].favorites.add(users[2])
        recipes[3].favorites.add(users[2])

        assert recipes[0].favorites.count() == 1
        assert recipes[2].favorites.count() == 2  # Two users favorited this recipe
        print("- Favorites added successfully ✔")
        return True
    except Exception as e:
        error_message = f"Error adding favorites: {e}"
        print(error_message)
        return False


def clear_database():
    """Delete all existing data from the database."""
    try:
        Like.objects.all().delete()
        Review.objects.all().delete()
        Recipe.objects.all().delete()
        Category.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        print("- Database cleared successfully ✔")
        return True
    except Exception as e:
        error_message = f"Error clearing database: {e}"
        print(error_message)
        return False


if __name__ == "__main__":
    print("Starting population script...")
    clear_database()

    add_users(users)
    add_categories(categories)
    add_recipes(recipes)
    add_reviews(reviews)
    add_likes(likes)
    add_favorites()

    print("Population completed! 🎉")

    # Summary of created data
    print("\nSummary:")
    print(f"- Users: {User.objects.count()}")
    print(f"- Categories: {Category.objects.count()}")
    print(f"- Recipes: {Recipe.objects.count()}")
    print(f"- Reviews: {Review.objects.count()}")
    print(f"- Likes: {Like.objects.count()}")