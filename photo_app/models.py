from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    email_validator = EmailValidator()
    phone_number = models.CharField(max_length=12, blank=True)
    email = models.EmailField(
        ("email address"),
        unique=False,
        blank=False,
        null=False,
        validators=[email_validator],
    )
    sity = models.CharField(max_length=12, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, verbose_name="Фото профиля"
    )
    on_the_list = models.BooleanField(default=False)

    def get_posts(self, order_by="-created_at", limit=20):
        return Post.objects.filter(author=self).order_by(order_by).limit(limit)

    def is_subscriber_of(self, other: "User") -> bool:
        """Проверить подписан ли other(requesr.user) на выбранного пользователя(self)"""

        return self.subscri_to_set.filter(subscriber=other).exists()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def upload_to_prefix(instance, filename):
    # Задать путь файлу поста
    prefix = instance.author.username[:1]
    return f"{prefix}/post_images/{filename}"


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_prefix)  # получить путь
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Получить хештег из описания"""

        text = self.caption.split()
        tags = [t.replace("#", "") for t in text if t.startswith("#")]
        tegs_for_post = [Tag(name=tag) for tag in tags]
        list_tags = Tag.objects.bulk_create(tegs_for_post)
        super().save(*args, **kwargs)
        self.tags.add(*list_tags)

    def __str__(self):
        return self.caption[:50]


# ----------------------------------------------------------------------------


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")

    # def save(self, *args, **kwargs):
    #     super(self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        # unique_together = ("post", "author")

    def comment_list(self, post):
        lst_obj = Comment.objects.filter(post=post).values_list("text", flat=True)
        comment_list_template = [f"{comment}\n" for comment in lst_obj]
        return comment_list_template

    def __str__(self):
        return self.text[:50]  # Показать первые 50 символов


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, related_name="subscri_set", on_delete=models.CASCADE
    )  # кто подписывается
    subscribed_to = models.ForeignKey(
        User, related_name="subscri_to_set", on_delete=models.CASCADE
    )  # на кого подписываются

    class Meta:
        unique_together = ("subscriber", "subscribed_to")
        verbose_name = "Кто подписался"
        verbose_name_plural = "На кого подписаны"

        indexes = [
            models.Index(fields=["subscriber"]),
            models.Index(fields=["subscribed_to"]),
            # Можно добавить индекс для парного использования полей
            models.Index(fields=["subscriber", "subscribed_to"]),
        ]

    # def __str__(self):
    #     return f"{self.subscriber} -> {self.subscribed_to}"

    # def __str__(self):
    #     return f"{self.subscriber}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("like", "Like"),
        ("new_post", "New_Post"),
    )

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_ot_kogo"
    )  # от кого

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_komy"
    )  # кому
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_object_id = models.PositiveIntegerField()
