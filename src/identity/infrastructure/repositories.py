"""Django ORM implementation of the identity repository interface.

This class satisfies the contract defined in identity.domain.repositories
using Django's ORM. It is the only place in the identity bounded context
that issues database queries for user accounts directly.
"""

from identity.models import CustomUser


class UserRepository:
    """IUserRepository backed by the Django ORM."""

    def get_by_id(self, user_id: int) -> CustomUser:
        return CustomUser.objects.get(pk=user_id)

    def get_by_email(self, email: str) -> CustomUser:
        return CustomUser.objects.get(email=email)

    def save(self, user: CustomUser) -> CustomUser:
        user.save()
        return user
