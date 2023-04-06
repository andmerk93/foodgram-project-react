from django.contrib.auth import get_user_model
from django.db import models

from core.models import Recipe

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_subscribed',
        verbose_name='Кто подписался'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_followed',
        verbose_name='На кого подписался'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'Flw: {self.user.username}->{self.following.username}'[:30]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self) -> str:
        return f'Fav: {self.user.username}->{self.recipe.name}'[:30]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупки'

    def __str__(self) -> str:
        return f'Shp: {self.user.username}->{self.recipe.name}'[:30]
