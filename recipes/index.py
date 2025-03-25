import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django import register
from recipes.models import Recipe
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime

class RecipeIndex(AlgoliaIndex):
    name = 'recipe'

    fields = (
        'title',
        'description',
        'ingredients',
        'instructions',
        'prep_time',
        'cook_time',
        'servings',
        'slug',
    )

    settings = {
        'searchableAttributes': [
            'title',
            'category',
            'description',
        ],
        'attributesForFaceting': [
            'title',
            'tags_indexing',
            'description',
            'category_indexing',
        ],
        'queryType': 'prefixLast',
        'advancedSyntax': True,
        'highlightPreTag': '<mark>',
        'highlightPostTag': '</mark>',
        'hitsPerPage': 15,
        'customRanking': [
            "desc(likes)",
        ],
    }

    index_name = 'recipes'

    def get_attributes(self, instance, attributes):
        print(f"Indexing {instance}...")
        for key, value in attributes.items():
            if isinstance(value, Recipe._meta.get_field(key).related_model):
                # Convert category to string
                attributes[key] = str(value)
                
            # Convert datetime fields to string format
            elif isinstance(value, datetime):
                attributes[key] = value.isoformat()
                
        return attributes