from rest_framework import serializers
from djoser.serializers import UserSerializer

from core.models import Tag, Recipe, Ingredient, IngredientsInRecipe
from users.models import Favourite, Follow, User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


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


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            'username',
            'first_name',
            'last_name',
#            'is_subscribed'  # =following
        )


class RecipeSerializer(serializers.ModelSerializer):
#    is_favourited = 
#    is_in_shopping_cart = 
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientsinrecipe',
        many=True
    )
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'
#        fields = ('id', 'name', 'tags')
#        read_only_fields = ('',)


class RecipeMinifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        source='following.email',
        required=False
    )
    id = serializers.IntegerField(
        source='following.id',
        required=False
    )
    username = serializers.CharField(
        source='following.username',
        required=False
    )
    first_name = serializers.CharField(
        source='following.first_name',
        required=False
    )
    last_name = serializers.CharField(
        source='following.last_name',
        required=False
    )
#    is_subscribed
    recipes = RecipeMinifiedSerializer(
        source='following.recipes',
        many=True,
        required=False
    )
    recipes_count = serializers.IntegerField(
        source='following.recipes.count',
        required=False
    )

    class Meta:
        model = Follow
        fields = CustomUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )
