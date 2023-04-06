from django.contrib.admin import ModelAdmin, site, TabularInline
from django.contrib.auth.admin import UserAdmin

from .models import Ingredient, IngredientsInRecipe, Recipe, Tag
from .models import TagsInRecipe, User


class RecipeIngredientInline(TabularInline):
    model = IngredientsInRecipe
    min_num = 1


class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')


class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time',)
    search_fields = ('text', 'name')
    list_editable = ('author', 'name', 'cooking_time')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientInline,)


class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_editable = ('name', 'slug', 'color')
    search_fields = ('name', 'slug', 'color')


class TagsInRecipeAdmin(ModelAdmin):
    list_display = ('id', 'recipe', 'tag')
    list_editable = ('recipe', 'tag')


class IngredientsInRecipeAdmin(ModelAdmin):
    list_display = ('id', 'recipe', 'amount', 'ingredient')
    list_editable = ('recipe', 'amount', 'ingredient')


class CustomUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('email', 'username')


PAIRS = [
    (Tag, TagAdmin),
    (Ingredient, IngredientAdmin),
    (Recipe, RecipeAdmin),
    (IngredientsInRecipe, IngredientsInRecipeAdmin),
    (TagsInRecipe, TagsInRecipeAdmin),
    (User, CustomUserAdmin),
]

site.unregister(User)

for i in PAIRS:
    site.register(*i)
