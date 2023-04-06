from io import StringIO

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import renderers, status, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from api import serializers
from api.permissions import FoodgramCurrentUserOrAdminOrReadOnly
from core.models import Tag, Ingredient, Recipe
from users.models import Favorite, Follow, ShoppingCart, User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (FoodgramCurrentUserOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'tags', 'author', 'is_favorited', 'is_in_shopping_cart'
    )


class SubscriptionListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return user.is_subscribed.all().select_related('following')


class SubscriptionCreateDestroyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubscriptionSerializer
    http_method_names = ['post', 'delete']

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return self.get_user().is_followed.all()

    def perform_create(self, serializer):
        user = self.request.user
        following = self.get_user()
        if (
            following == user
            or Follow.objects.filter(
                user=user, following=following
            ).exists()
        ):
            raise ValidationError(
                'Ошибка: подписка уже создана '
                + 'или вы пытаетесь подписаться на себя'
            )
        serializer.save(following=following, user=user)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        following = self.get_user()
        instance = get_object_or_404(Follow, user=user, following=following)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RecipeMinifiedSerializer
    http_method_names = ['post', 'delete']
    model = Favorite

    def get_queryset(self):
        return get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))

    def create(self, request, *args, **kwargs):
        user = self.request.user
        recipe = self.get_queryset()
        if not self.model.objects.filter(user=user, recipe=recipe).exists():
            self.model.objects.create(user=user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = self.get_queryset()
        instance = get_object_or_404(self.model, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(FavoriteViewSet):
    model = ShoppingCart


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data


@api_view(['GET'])
@renderer_classes([PlainTextRenderer])
def download_shopping_cart(request):
    user = request.user
    cart = get_list_or_404(
        ShoppingCart.objects.select_related('recipe').prefetch_related(
            'recipe__ingredients_in_recipe'
        ),
        user=user
    )
    ingredients = []
    for i in cart:
        ingredients.extend(
            i.recipe.ingredients_in_recipe.all()
        )
    ingredients_dict = {}
    for i in ingredients:
        ingredients_dict[i.ingredient_id] = 0
    for i in ingredients:
        ingredients_dict[i.ingredient_id] += i.amount
    data = StringIO()
    for i in ingredients_dict:
        ingredient = Ingredient.objects.get(id=i)
        text = f'{ingredient.name} ({ingredient.measurement_unit}) —'
        text += f' {ingredients_dict[i]} \n'
        data.write(text)
    data.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="list.txt"',
    }
    return Response(data, status=status.HTTP_200_OK, headers=headers)
