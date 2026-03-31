"""Application use cases for the identity bounded context.

Each use case class orchestrates domain logic and persistence
without leaking infrastructure concerns into the domain.
"""

from django.db import transaction

from fleet.models import Driver
from identity.models import CustomUser


class RegisterUser:
    """Register a new user and provision their driver profile.

    Creates a CustomUser account and an associated Driver record within
    a single atomic transaction so that neither can exist without the other.
    """

    def execute(
        self, email: str, password: str, given_names: str, surnames: str
    ) -> CustomUser:
        """Create a user account and a linked driver profile.

        Args:
            email: The user's email address; used as the login identifier.
            password: The plain-text password; hashed before storage.
            given_names: First and/or middle names.
            surnames: Family name(s).

        Returns:
            The newly created CustomUser instance.
        """
        with transaction.atomic():
            custom_user = CustomUser.objects.create_user(  # type: ignore
                email=email,
                password=password,
                given_names=given_names,
                surnames=surnames,
            )

            Driver.objects.create(user=custom_user)

        return custom_user
