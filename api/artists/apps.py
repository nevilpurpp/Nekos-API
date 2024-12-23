from django.apps import AppConfig


class ArtistsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "artists"

    def ready(self) -> None:
        import artists.signals
