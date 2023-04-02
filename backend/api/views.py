from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ValidationError
#from djoser.permissions import CurrentUserOrAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from api import serializers
from api.permissions import FoodgramCurrentUserOrAdminOrReadOnly
from core.models import Tag, Ingredient, Recipe
from users.models import Favourite, Follow, User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
#    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
#    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (FoodgramCurrentUserOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags', 'author', )#'is_favorited', 'is_in_shopping_cart')


class SubscriptionListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SubscriptionSerializer
#    permission_classes = (IsAuthenticated,)
#    filter_backends = (SearchFilter,)
#    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()


class SubscriptionCreateDestroyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubscriptionSerializer
#    permission_classes = (IsAuthenticated,)
    http_method_names = ['post', 'delete']

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return self.get_user().following.all()

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
                'Ошибка: подписка уже создана ' +
                'или вы пытаетесь подписаться на себя'
            )
        serializer.save(following=following, user=user)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        following = self.get_user()
        instance = get_object_or_404(Follow, user=user, following=following)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
