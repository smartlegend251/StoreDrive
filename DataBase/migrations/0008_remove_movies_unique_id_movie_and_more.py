# Generated by Django 5.0.4 on 2024-05-21 13:25

import DataBase.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0007_movies_unique_id_movie_music_unique_id_music_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='unique_id_movie',
        ),
        migrations.RemoveField(
            model_name='music',
            name='unique_id_music',
        ),
        migrations.RemoveField(
            model_name='photos',
            name='unique_id_photo',
        ),
        migrations.RemoveField(
            model_name='videos',
            name='unique_id_video',
        ),
        migrations.AddField(
            model_name='movies',
            name='unique_id',
            field=models.CharField(default=DataBase.models.unique_ids, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='music',
            name='unique_id',
            field=models.CharField(default=DataBase.models.unique_ids, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='photos',
            name='unique_id',
            field=models.CharField(default=DataBase.models.unique_ids, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='videos',
            name='unique_id',
            field=models.CharField(default=DataBase.models.unique_ids, max_length=10, unique=True),
        ),
    ]