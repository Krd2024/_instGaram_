from django.apps import AppConfig

# from photo_app import signals


class PhotoAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "photo_app"

    def ready(self):

        import photo_app.signals  # noqa
