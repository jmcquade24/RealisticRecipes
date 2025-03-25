from django.apps import AppConfig

class RecipesConfig(AppConfig):
    name = 'recipes'

    def ready(self):
        from algoliasearch_django import register
        from algoliasearch_django import save_record
        from recipes.models import Recipe
        from recipes.index import RecipeIndex
        register(Recipe, RecipeIndex)
        #recipes = Recipe.objects.all()

        #for recipe in recipes:
        #    save_record(recipe)
