# Generated by Django 5.1 on 2024-08-27 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0008_alter_comment_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
    ]
