from photo_app.forms import CommentForm, PhotoForm, PostForm
from photo_app.serializers import PostSerializer, TagSerializer, UserSerializer
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from collections import Counter

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from .serializers import CreateUserSerializer


from photo_app.models import Comment, Post, Tag, User
from photo_app.processor.postgre_data import (
    create_delete_like,
    delete_post_gallery,
    get_all_posts_in_tag,
    get_main,
    get_notification_in_user,
    get_subscribed_to,
    get_subscriber,
    get_user_friends,
    get_user_profile,
    notification_is_read,
    subscription_create,
)


def index(request):
    """Главная страница: все пользователи,все посты"""

    users = get_main()
    # print(users, "<<< ---------------- index")
    return render(request, "other/index.html", {"users": users})


def user_profile(request, username, notification=False):
    """Показать выбранного пользователя и все его посты.
    Если notification = True, отметить уведомления о ноых постах
    как прочитанные"""

    if not request.user.is_authenticated:
        # messages.success(request, "На регистрацию!")
        return redirect("register")

    if notification:
        notification_is_read(request, username)

    user, subscriber = get_user_profile(request, username)
    print(user, "<--- context", " ", subscriber, "< --- subscriber")

    return render(
        request,
        "other/profile.html",
        {"user": user, "subscriber": subscriber},
    )


# @login_required
def upload_photo(request):
    """Добавить фото профиля"""

    user = request.user
    if request.method == "POST":
        # form = PhotoForm(request.POST, request.FILES)
        form = PhotoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():

            uploaded_file = request.FILES["profile_picture"]
            print(uploaded_file, "<<< ----- profile_picture")

            form.save()

            return redirect("index")
    else:
        form = PhotoForm(instance=user)

    return render(request, "other/upload_photo.html", {"form": form})


def upload_photo_gallery(request):
    """Добавить фото(пост) в галерею.Проверка на хештег в signals.py"""

    user = request.user
    try:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                form.save()

                return redirect("index")
        else:
            form = PostForm(instance=user)
    except Exception as e:
        print(e, "<<<<<< e")

    return render(request, "other/upload_gallery.html", {"form": form})


def like_counter(request, post_id):
    """Счётчик лайков"""

    if not request.user.is_authenticated:
        return JsonResponse({"success": 0, "answer": 0})

    if request.method == "POST":
        count_like = create_delete_like(request.user, post_id)
    return JsonResponse({"success": 1, "answer": count_like})


def subscription(request, username):
    """Подписаться на пользователя"""

    result = subscription_create(request.user, username)
    if result:
        return JsonResponse({"success": 1, "answer": "Вы подписаны"})
    else:
        return JsonResponse({"success": 0, "answer": "Подписаться"})


def subscribed_to(request):
    """Показать подписчиков"""

    user = request.user
    subscribed_to_ = get_subscribed_to(user)
    # for i in subscribed_to_:
    #     print(i.subscriber, "< --- subscriber")
    # print(subscribed_to, "<----------------- subscribed_to")
    return render(
        request, "other/subscribed_to.html", {"subscribed_to_user": subscribed_to_}
    )


def subscriber(request):
    """Показать подписки"""

    try:
        user = request.user
        subscriber_ = get_subscriber(user)

    except Exception as e:
        print(e)
    return render(request, "other/subscriber.html", {"subscriber_user": subscriber_})


def add_comment(request, post_id):
    """Создать комментарий"""

    if not request.user.is_authenticated:
        return redirect("register")

    print(post_id, "<< -- post_id")
    try:
        post = Post.objects.get(id=post_id)
        if request.method == "POST":
            form = CommentForm(request.POST)
            # author = request.POST.get("author")
            # comment_text = request.POST.get("comment")
            # user = Post.objects.get(id=post_id)

            # # user_comment_to = User.objects.get(username=user.author.username)

            comment, created = Comment.objects.update_or_create(
                post=post, author=request.user, text=request.POST.get("comment")
            )
            if created:
                print("Комментарий был создан.")
            else:
                print("Комментарий был обновлен.")
            return redirect("user_profile", post.author)
        else:
            form = CommentForm()
            comments = Comment.objects.filter(post=post)
            print(comments, "< -- Comment")

    except Exception as e:
        print(e)

    return render(
        request,
        "other/comment_form.html",
        {
            "form": form,
            "comments": comments,
            "post": post,
        },
    )


def all_posts_in_tag(request, tag_name):
    """Показать все посты для тега"""

    context = get_all_posts_in_tag(tag_name)
    print(context, "<<< ----------- context для шаблона -----------")

    return render(request, "other/all_posts_tag.html", {"all_posts": context})


# def all_tags_in_post(request, post_id):
#     post = Post.objects.get(id=post_id)
#     tags_for_post = post.tags.all()


# @cache_page(600, cache="default", key_prefix="")
def frands(request):
    print("< ---------------- Друзья ")
    try:
        user = request.user
        subscribed_to_ = get_subscribed_to(user)
        subscribed = get_subscriber(user)
        frands = get_user_friends(subscribed_to_, subscribed)
        return render(request, "other/frands.html", {"frands": frands})
    except Exception as e:
        print(e)


def delete_gallery_post(request, post_id):
    """Удалить пост"""

    res = delete_post_gallery(post_id)
    if res:
        messages.success(request, "Пост успешно удалён!")
        return redirect("user_profile", request.user)
    messages.success(request, "Что-то пошло не так!")
    return redirect("user_profile", request.user)


def notification(request):
    """Получить все не прочитанные уведомления пользователя"""

    username = request.user.username
    notifications = get_notification_in_user(username)

    if not notifications:
        messages.success(request, "У вас нет новых уведомлений.")
    # Подсчитываем уведомления от каждого отправителя
    sender_counts = Counter(notification.sender for notification in notifications)
    # Создать словарь => пользователь : кол-во новых постов
    sender_counts_dict = {str(sender): count for sender, count in sender_counts.items()}

    context = {
        "notifications": notifications,
        "sender_counts": sender_counts_dict,
    }

    return render(request, "other/notification.html", context)


#             ---------------------- api -----------------------------------

"""
GET /api/users/ — для получения списка пользователей
POST /api/users/ — для создания нового пользователя
GET /api/users/{id}/ — для получения информации о конкретном пользователе
PUT /api/users/{id}/ — для обновления информации о пользователе
PATCH /api/users/{id}/ — для частичного обновления информации о пользователе
DELETE /api/users/{id}/ — для удаления пользователя

================================================================================

list(): Обрабатывает GET-запросы на /tags/, возвращает список всех объектов.
retrieve(): Обрабатывает GET-запросы на /tags/<id>/, возвращает конкретный объект.
create(): Обрабатывает POST-запросы на /tags/, создаёт новый объект.
update(): Обрабатывает PUT-запросы на /tags/<id>/, обновляет объект.
partial_update(): Обрабатывает PATCH-запросы на /tags/<id>/, частично обновляет объект.
destroy(): Обрабатывает DELETE-запросы на /tags/<id>/, удаляет объект.

"""


# ----------------------------------------------------------------
class UserApiView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get"]


class TagsApiView(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    # queryset = Tag.objects.values_list("name", flat=True)
    serializer_class = TagSerializer
    http_method_names = ["get"]

    # Переопределить для получения только имён
    def list(self, request, *args, **kwargs):
        # Получаем список имен
        names = Tag.objects.values_list("name", flat=True)
        return Response(names)

    # -------------------------------------------------- стандартное поведение ------------------------
    # Срабатыает при обращении к конкретному тегу
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance, "<<< ==== Instance")
        serializer = self.get_serializer(instance)
        data = serializer.data

        data["additional_info"] = "some additional data"  # добавиь
        return Response(data)

    # ------------------------------------------------------------------------------------------------


class PostlApiView(viewsets.ReadOnlyModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ["get"]

    #                      - тоже самое -


class PostListView(APIView):
    print("APIPost")
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]
