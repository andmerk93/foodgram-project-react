from django.contrib.admin import ModelAdmin, site

from .models import Follow, Favorite, ShoppingCart


class FollowAdmin(ModelAdmin):
    list_display = ('id', 'user', 'following')
    list_editable = ('user', 'following')


class FavoriteAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_editable = ('user', 'recipe')


site.register(Follow, FollowAdmin)
site.register(Favorite, FavoriteAdmin)
site.register(ShoppingCart, FavoriteAdmin)
