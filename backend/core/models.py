from django.contrib.auth import get_user_model
from django.db import models

# from users.models import User

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Tag', max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    color = models.CharField(max_length=7)


class Ingredient(models.Model):
    name = models.CharField('Ingredient', max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    name = models.CharField('Recipe', max_length=200)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    cooking_time = models.PositiveSmallIntegerField('Time (min)')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
#    tag = models.ForeignKey(
#        Tag,
#        on_delete=models.CASCADE,
#        related_name='recipes',
#    )


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
#        verbose_name='Кто подписался'
    )
    quantity = models.PositiveSmallIntegerField()
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
#        verbose_name='На кого подписался'
    )


class TagInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags',
#        verbose_name='Кто подписался'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes',
#        verbose_name='На кого подписался'
    )
