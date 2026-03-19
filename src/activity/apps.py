from django.apps import AppConfig


class ActivityConfig(AppConfig):
    name = "activity"

    def ready(self):
        import activity.infrastructure.admin  # noqa: F401
