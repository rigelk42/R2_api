from django.apps import AppConfig


class FleetConfig(AppConfig):
    """Django app config for the fleet bounded context.

    Manages driver profiles and vehicles. The admin module is imported
    in ready() so that its ModelAdmin registrations are applied after
    all models have been loaded.
    """

    name = "fleet"

    def ready(self):
        import fleet.infrastructure.admin  # noqa: F401
