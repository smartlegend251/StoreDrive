# Generated by Django 5.0.4 on 2024-05-12 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0008_myuser_is_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='server_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]