from photo_app.models import User


def cart_user(request):
    """Виджет пользователя"""

    if request.user.is_authenticated:
        username = User.objects.get(username=request.user.username)

        # Проверить наличие уведомлений
        user_notification_komy = username.notification_komy.filter(
            is_read=False
        ).exists()
        if user_notification_komy:
            print("ЕСТЬ УВЕДОМЛЕНИЯ")
            notification = True
        else:
            print("НЕТ УВЕДОЛЕНИЙ")
            notification = False

        return {"user_context": username, "notification": notification}
        # return {"user_context": username, "user_subscription": user_subscription}
    return {"x": 0}


def count_like(request):
    # count_like = Like.objects.all()
    return {"count_like": 7777777}
    # return {"count_like": count_like}
