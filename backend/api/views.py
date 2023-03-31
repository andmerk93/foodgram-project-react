from rest_framework import permissions, viewsets
from djoser.permissions import CurrentUserOrAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from api import serializers
from core.models import Tag, Ingredient, Recipe


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (CurrentUserOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)
