from rest_framework import viewsets
#from rest_framework import permissions
from rest_framework.permissions import AllowAny
#from djoser.permissions import CurrentUserOrAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from api import serializers
from api.permissions import FoodgramCurrentUserOrAdminOrReadOnly
from core.models import Tag, Ingredient, Recipe


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (FoodgramCurrentUserOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags', 'author', )#'is_favorited', 'is_in_shopping_cart')
