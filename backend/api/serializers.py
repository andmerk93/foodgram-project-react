from rest_framework import serializers

from core.models import Tag, Recipe, Ingredient, IngredientsInRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
#        fields = ('id', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id'
    )
    name = serializers.CharField(
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
#    is_favourited = 
#    is_in_shopping_cart = 
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientsinrecipe',
        many=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'
#        fields = ('id', 'name', 'tags')
#        read_only_fields = ('',)
