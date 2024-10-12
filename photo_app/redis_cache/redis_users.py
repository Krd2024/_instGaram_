import redis
from django.conf import settings
from django.core.cache import cache

from photo_app.models import User

redis_instance = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def get_user_all_redis(user_id=None):
    """Получить всех из редис"""

    # cache.delete("all_users")
    users = cache.get("all_users")
    print(users, "< ------------------- users из redis")
    if users is None:
        # users = User.objects.all() <<< --- 800 ms + 63 запроса SQL(30ms)
        users = User.objects.prefetch_related(
            "post_set__like_set"
        ).all()  # <<< --- 200 ms + 4 SQL запроса(3.5ms)

        print(users, "< -------------------  users из sqlite")
        cache.set("all_users", users, timeout=300)
    return users


def get_user_profile_redis(request, username):
    """Вернуть объект выбранного пользователя"""
    try:
        # cache.delete(username)
        cached_data = cache.get(username)

        if cached_data is None:

            user = User.objects.filter(
                username=username
            )  # Time 300ms + 16 SQL(12.3ms) / с редисом Time 200 + 11 SQL(4ms)

            # Проверить подписку пользователя(request.user) на выбранного пользователя
            subscriber = user[0].is_subscriber_of(request.user)
            print(user, "< ------------------- user из sqlite")
        else:
            user = cached_data.get("user")
            subscriber = cached_data.get("subscriber")
            print(user, "< -------------- user из redis")
    except Exception as e:
        print(e, " <<< ------------- e")

    cache.set(username, {"user": user, "subscriber": subscriber}, timeout=30)

    return user, subscriber
