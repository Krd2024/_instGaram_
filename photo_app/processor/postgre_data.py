import json
from django.db import IntegrityError
from django.http import Http404, HttpResponse

from photo_app.redis_cache.redis_users import get_user_all_redis, get_user_profile_redis
from ..models import *
from django.shortcuts import get_object_or_404


def get_main():

    users = get_user_all_redis()  # получить из редиса

    return users


def get_user_profile(request, username):
    """Вернуть объект выбранного пользователя"""
    # user = User.objects.filter(username=username)
    # subscriber = user[0].is_subscriber_of(request.user)
    # return user, subscriber

    return get_user_profile_redis(request, username)  # получить из редиса


# ----------------------------------------------------------------

import threading
import queue

# ----------------------------------------------------------------
import redis
from django.conf import settings
from django.core.cache import cache

from photo_app.models import User

#                           --------

redis_instance = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def create_delete_like(user, post_id):
    """Поставить,убрать лайк"""

    print(user, post_id, "user - post_id")
    try:
        post = Post.objects.get(id=post_id)
        if post.author == user:
            return Like.objects.filter(post=post).count()

        like, created = Like.objects.get_or_create(post=post, user=user)

        if created:
            print("Like успешно добавлено")
            # cache.set("choice_user", {"subscriber": True})

            count_like = Like.objects.filter(post=post).count()
            return count_like
        else:
            print("Like удалён")
            like.delete()

            count_like = Like.objects.filter(post=post).count()
            # queue.put(count_like)
            return count_like
    except IntegrityError:
        print("Произошла ошибка при попытке создать лайк")

    return HttpResponse(1)


# ----------------------------------------------------------------
def subscription_create(request_user, user):
    """Подписаться или отменить подписку"""

    # print(request_user, user)
    if request_user.username == user:
        return False

    subscriber = User.objects.get(username=request_user)
    subscribed_to = User.objects.get(username=user)

    subscription, created = Subscription.objects.get_or_create(
        subscriber=subscriber, subscribed_to=subscribed_to
    )

    # Если есть подписка добавить - True в redis
    if created:
        print("Подписка успешно создана")

        cached_data = cache.get(user)
        cached_data["subscriber"] = True
        cache.set(user, cached_data, timeout=300)
        return True

    # Если нет подписка добавить - False в redis
    else:
        print("Подписка отменена")

        subscription.delete()
        cached_data = cache.get(user)
        cached_data["subscriber"] = False
        cache.set(user, cached_data, timeout=300)


def get_subscribed_to(user):
    """Подписчики request.user"""

    user = User.objects.get(username=user.username)
    # print(user)
    return user.subscri_to_set.all()


def get_subscriber(user):
    """Подписки request.user"""

    user = User.objects.get(username=user.username)
    # print(user)
    return user.subscri_set.all()


def get_all_posts_in_tag(tag_name):
    """Все посты тега"""
    # cache.delete("get_all_posts_in_tag")
    try:
        all_tags = cache.get(tag_name)

        if all_tags[0] != tag_name:

            all_tags = Tag.objects.filter(name=tag_name)

            cache.set(tag_name, all_tags)
            print(all_tags[0], "<<<<<< --------------- tag_name из sql ")

        print(all_tags, "<<<<<< --------------- tag_name из редис")
    except Exception as e:

        all_tags = Tag.objects.filter(name=tag_name)
        cache.set(tag_name, all_tags)
    return all_tags
    # return Tag.objects.filter(name=tag_name)


# <QuerySet [<Tag: природа>, <Tag: природа>]>

# Получаем пост
"post = get_object_or_404(Post, id=post_id)"

# Получаем всех пользователей, которые лайкнули пост
"liked_users = User.objects.filter(likes__post=post)"

# Проверяем, есть ли уже лайк от этого пользователя на этот пост
"""
try:
    like, created = Like.objects.get_or_create(post=post, user=user)
    if created:
        print("Like added successfully")
    else:
        print("User has already liked this post")
except IntegrityError:
    print("An error occurred while trying to create the like")

"""


def get_user_friends(subscribed_to_, subscribed):
    """Список друзей"""

    subscribed_to = [subsc.subscriber for subsc in subscribed_to_]
    subscriber = [subsc.subscribed_to for subsc in subscribed]
    print(subscribed_to, subscriber)

    subscribers_set = set(subscribed_to)
    subscribed_set = set(subscriber)

    frands = subscribers_set.intersection(subscribed_set)
    print(frands, "<<<<<<<<<< --- frands")

    return frands


def delete_post_gallery(post_id):
    try:
        Post.objects.get(id=post_id).delete()
        return True
    except Exception as e:
        print(e)
        return False


# instance из сигнала
def notification_in_signal(instance):
    """Создать уведомления для подписчиков о новом посте"""
    try:
        author_post = instance.author
        print(author_post, "< ----- author")
        user = User.objects.filter(username=author_post).first()
        subscribers = (
            user.subscri_to_set.all()
        )  # Получить всех подписчиков пользователя

        notifications = []
        for subscriber in subscribers:
            # print(type(subscriber.subscriber))
            notification = Notification(
                sender=user,  # пользователь, на которого подписаны
                recipient=subscriber.subscriber,  # Получатель - подписчик
                notification_type="new_post",
                related_object_id=instance.id,  #  ID связанного объекта
            )
            notifications.append(notification)

            # Сохранить
        Notification.objects.bulk_create(notifications)
    except Exception as e:
        print(e)


def get_notification_in_user(username):
    """Получить все не прочитанные уведомления пользователя"""

    try:
        user = User.objects.get(username=username)  # Получаем пользователя
        notifications = user.notification_komy.filter(
            is_read=False
        )  # Получаем все уведомления, отправленные  пользователю

        print(notifications, "< ---------------- notifications")
        return notifications
    except Exception as e:
        print(e)
        return False


def notification_in_signal_delete(instance):
    """Удалить объект уведомления при удалении поста"""

    try:
        notification = Notification.objects.filter(related_object_id=instance.id)
        print(notification, "< ----------------- notification-delete")
        notification.delete()
    except Notification.DoesNotExist:
        print("DoesNotExist")
        raise Http404("Уведомление не найдено.")


def notification_is_read(request, username):
    print(f"Удалить увед. для {request.user} от {username}")
    user_obj = User.objects.get(username=username)
    update = Notification.objects.filter(
        sender=user_obj, recipient=request.user
    ).update(is_read=True)
    print(f"Отметить прочитанным: {update} уведомления")
    # for up_date in update:
    #     up_date.is_read = True
    #     up_date.save()
