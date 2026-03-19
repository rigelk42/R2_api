from django.apps import AppConfig


class FleetConfig(AppConfig):
    name = "fleet"

    def ready(self):
        import fleet.infrastructure.admin  # noqa: F401
