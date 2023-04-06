from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    color = models.CharField(max_length=7)

    class Meta:
        ordering = ['slug']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(300),
            MinValueValidator(1)
        ]
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsInRecipe',
        related_name='recipes',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
        ]
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Игнр. в рецептах'
        verbose_name_plural = 'Игнр. в рецептах'

    def __str__(self) -> str:
        text = (
            f'IR: {self.amount}x {self.ingredient.name}' +
            f'->{self.recipe.name}'
        )
        return text[:30]


class TagsInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Теги на рецептах'
        verbose_name_plural = 'Теги на рецептах'

    def __str__(self) -> str:
        return f'TR: {self.tag.name}->{self.recipe.name}'[:30]
