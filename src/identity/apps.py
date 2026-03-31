from django.apps import AppConfig


class IdentityConfig(AppConfig):
    """Django app config for the identity bounded context.

    Handles user authentication and registration. The admin module is
    imported in ready() so that its ModelAdmin registrations are
    applied after all models have been loaded.
    """

    name = "identity"

    def ready(self):
        import identity.infrastructure.admin  # noqa: F401
