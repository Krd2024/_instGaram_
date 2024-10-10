from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from photo_app.processor.postgre_data import (
    notification_in_signal,
    notification_in_signal_delete,
)
from .models import Post, User


def clear_authors_count_cache():
    """Очистить кеш при создании,
    удалении поста,при регистрации
    нового пользователя
    """

    cache.delete("all_users")


@receiver(post_save, sender=User)
def pre_save_user(sender, instance, created, **kwargs):

    if created or instance.profile_picture is not None:
        print(instance.profile_picture, "<---------profile_picture")
        clear_authors_count_cache()
        print("НОВЫЙ ПОЛЬЗОВАТЕЛЬ")


@receiver(post_save, sender=Post)
def pre_save_user_post(sender, instance, created, **kwargs):

    if instance.image:
        notification_in_signal(instance)  # Создать уведомления для подписчиков
        clear_authors_count_cache()  # Очистить кеш
        print("НОВЫЙ ПОСТ")


@receiver(post_delete, sender=Post)
def pre_delete_post(sender, instance, **kwargs):
    notification_in_signal_delete(instance)
    clear_authors_count_cache()
    print("ПОСТ УДАЛЁН")
