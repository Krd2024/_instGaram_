# Generated by Django 5.1 on 2024-08-26 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0007_alter_comment_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('post', 'author')},
        ),
    ]
