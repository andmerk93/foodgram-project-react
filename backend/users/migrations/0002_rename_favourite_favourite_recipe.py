# Generated by Django 4.1.7 on 2023-03-25 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favourite',
            old_name='favourite',
            new_name='recipe',
        ),
    ]
