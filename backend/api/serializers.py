from rest_framework import serializers

from core.models import Tag, Recipe, Ingredient, IngredientInRecipe


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
    amount = serializers.IntegerField(
        source='IngredientInRecipe.get.amount',
#        read_only=True,
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
#        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
#    is_favourited = 
#    is_in_shopping_cart = 
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
#        fields = ('id', 'name', 'tags')
#        read_only_fields = ('',)
