from django.urls import include, path
from django.conf.urls.static import static

from django.conf import settings
from photo_app.auth_user import auth_login

# from serial_test import Get_cap

from .views import (
    CreateUserView,
    PostListView,
    PostlApiView,
    TagsApiView,
    UserApiView,
    add_comment,
    all_posts_in_tag,
    delete_gallery_post,
    frands,
    index,
    like_counter,
    notification,
    subscribed_to,
    subscriber,
    subscription,
    upload_photo_gallery,
    user_profile,
    upload_photo,
)

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"api/users", UserApiView)
router.register(r"api/tags", TagsApiView)
router.register(r"api/posts", PostlApiView)

urlpatterns = [
    #                 - API -
    path("test_api/", include(router.urls)),
    path("posts/", PostListView.as_view()),
    path("api/users/create/", CreateUserView.as_view(), name="create_user"),
    # path("api/get_cap/", Get_cap.as_view(), name="get_cap"),
    #                 -------
    path("", index, name="index"),
    path("login/", auth_login.login_view, name="login"),
    path("register/", auth_login.register_view, name="register"),
    path("logoutPage/", auth_login.logoutPage, name="logoutPage"),
    #
    path("profile/<str:username>/", user_profile, name="user_profile"),
    path("user/upload_photo/", upload_photo, name="upload_photo"),
    path("user/upload_gallery/", upload_photo_gallery, name="upload_gallery"),
    path(
        "user/delete_gallery/<int:post_id>",
        delete_gallery_post,
        name="delete_gallery_post",
    ),
    path(
        "user/profile/<str:username>/<str:notification>/",
        user_profile,
        name="user_profile",
    ),
    path("user/subscribed_to/", subscribed_to, name="subscribed_to"),
    path("user/subscriber/", subscriber, name="subscriber"),
    path("user/notification/", notification, name="notification"),
    path("user/frands/", frands, name="frands"),
    #
    path("like_counter/<int:post_id>/", like_counter, name="like_counter"),
    path("subscription/<str:username>/", subscription, name="subscription"),
    #
    path("add_comment/<int:post_id>/", add_comment, name="add_comment"),
    #
    path("posts_tag/<str:tag_name>/", all_posts_in_tag, name="all_posts_in_tag"),
    #
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
