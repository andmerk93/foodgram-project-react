from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
# from drf_base64.fields import Base64ImageField

from core.models import Tag, Recipe, Ingredient, IngredientsInRecipe
from users.models import Favorite, Follow, ShoppingCart, User


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
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        result = False
        user = self.context['request'].user
        if user.is_authenticated:
            result = Follow.objects.filter(user=user, following=obj).exists()
        return result


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = UserCreateSerializer.Meta.fields + (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class RecipeRetrieveSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredients_in_recipe',
        many=True
    )
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'

    def validator(self, obj, model):
        result = False
        user = self.context['request'].user
        if user.is_authenticated:
            result = model.objects.filter(user=user, recipe=obj).exists()
        return result

    def get_is_favorited(self, obj):
        return self.validator(obj, Favorite)

    def get_is_in_shopping_cart(self, obj):
        return self.validator(obj, ShoppingCart)


class RecipeMinifiedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientsListingSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientsListingSerializer(
        many=True,
        source='ingredients_in_recipe'
    )
#    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
#            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients_in_recipe')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
#        image = validated_data.pop('image')
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = ingredient['id']
            IngredientsInRecipe.objects.create(
                amount=amount, recipe=recipe, ingredient=ingredient
            )
        return recipe


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
    is_subscribed = serializers.SerializerMethodField()
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

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            following_id=self.context['request'].user.id,
            user_id=obj.following_id
        ).exists()
