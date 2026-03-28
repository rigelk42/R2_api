# Application use cases for the identity bounded context.
# Each use case class orchestrates domain logic and persistence
# without leaking infrastructure concerns into the domain.
from django.db import transaction

from fleet.models import Driver
from identity.models import CustomUser


class RegisterUser:
    def execute(
        self, email: str, password: str, given_names: str, surnames: str
    ) -> CustomUser:
        with transaction.atomic():
            custom_user = CustomUser.objects.create_user(  # type: ignore
                email=email,
                password=password,
                given_names=given_names,
                surnames=surnames,
            )

            Driver.objects.create(user=custom_user)

        return custom_user
