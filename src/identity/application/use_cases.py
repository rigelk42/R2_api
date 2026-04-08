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


class UpdateUser:
    """Update the name fields of an existing user account."""

    def execute(self, user: CustomUser, given_names: str, surnames: str) -> CustomUser:
        """Persist updated name fields for the given user.

        Only given_names and surnames are touched; all other fields,
        including the email and password, are left unchanged.

        Args:
            user: The CustomUser instance to update.
            given_names: Replacement given names.
            surnames: Replacement surnames.

        Returns:
            The updated CustomUser instance.
        """
        user.given_names = given_names
        user.surnames = surnames
        user.save(update_fields=["given_names", "surnames"])

        return user
