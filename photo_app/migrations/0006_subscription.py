# Generated by Django 5.1 on 2024-08-23 19:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_app', '0005_alter_post_options_remove_post_liked_users_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscri_to_set', to=settings.AUTH_USER_MODEL)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscri_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Кто подписался',
                'verbose_name_plural': 'На кого подписаны',
                'unique_together': {('subscriber', 'subscribed_to')},
            },
        ),
    ]
