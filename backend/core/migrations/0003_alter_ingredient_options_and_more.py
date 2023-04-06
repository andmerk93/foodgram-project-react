# Generated by Django 4.1.7 on 2023-04-06 14:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='ingredientsinrecipe',
            options={'ordering': ['id'], 'verbose_name': 'Игнр. в рецептах', 'verbose_name_plural': 'Игнр. в рецептах'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-id'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['slug'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterModelOptions(
            name='tagsinrecipe',
            options={'ordering': ['id'], 'verbose_name': 'Теги на рецептах', 'verbose_name_plural': 'Теги на рецептах'},
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='core.ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='core.recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(300), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='tagsinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_in_recipe', to='core.recipe'),
        ),
        migrations.AlterField(
            model_name='tagsinrecipe',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_in_recipe', to='core.tag'),
        ),
    ]
