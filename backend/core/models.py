from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    cooking_time = models.PositiveSmallIntegerField()
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

    def __str__(self):
        return self.name


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientsinrecipe',
    )
    amount = models.PositiveSmallIntegerField()
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientsinrecipe',
    )

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
        related_name='TagsInRecipe',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='TagsInRecipe',
    )

    def __str__(self) -> str:
        return f'TR: {self.tag.name}->{self.recipe.name}'[:30]
