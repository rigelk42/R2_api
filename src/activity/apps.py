from django.apps import AppConfig


class ActivityConfig(AppConfig):
    """Django app config for the activity bounded context.

    Tracks per-day driving activity entries across rideshare platforms.
    The admin module is imported in ready() so that its ModelAdmin
    registrations are applied after all models have been loaded.
    """

    name = "activity"

    def ready(self):
        import activity.infrastructure.admin  # noqa: F401
