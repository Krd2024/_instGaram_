# Generated by Django 5.1 on 2024-08-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0002_user_sity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_pics/', verbose_name='Фото профиля'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sity',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
