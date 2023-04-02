from django.urls import include, path, re_path

from djoser.views import UserViewSet

from rest_framework.routers import SimpleRouter

from api import views

api_router = SimpleRouter()
api_router.register('tags', views.TagViewSet, basename='tag')
api_router.register('ingredients', views.IngredientViewSet, basename='ingredient')
api_router.register('recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(api_router.urls),),
    path('auth/', include('djoser.urls.authtoken')),
    path("users/", UserViewSet.as_view({"get": "list"}), name="user_list"),
    path('users/', UserViewSet.as_view({'post': 'create'}), name="user_create"),
    path('users/me/', UserViewSet.as_view({'get': 'me'}), name="current_user"),
    path("users/set_password/", UserViewSet.as_view({"post": "set_password"}), name="set_password"),
    path("users/subscribtions/", views.SubscriptionListViewSet.as_view({"get": "list"}), name="subscriptions_list"),
    path("users/<str:id>/", UserViewSet.as_view({"get": "retrieve"}), name="user"),
    re_path(
        r'users/(?P<user_id>[\d]+)/subscribe/',
        views.SubscriptionCreateDestroyViewSet.as_view(
            {'post': 'create', 'delete': 'delete'}
        ),
        name="subscription_create_delete"
    ),
]
