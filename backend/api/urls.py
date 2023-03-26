from django.urls import include, path

from rest_framework.routers import SimpleRouter

from api import views

api_router = SimpleRouter()
api_router.register('tags', views.TagViewSet, basename='tag')
api_router.register('ingredients', views.IngredientViewSet, basename='ingredient')
api_router.register('recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(api_router.urls),),
]
