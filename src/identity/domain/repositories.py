"""Repository interface for the identity bounded context.

This Protocol defines the persistence contract that the domain and
application layers depend on. The concrete Django ORM implementation
lives in identity.infrastructure.repositories and is injected at runtime.

This inversion keeps the domain free of ORM and database concerns.
"""

from typing import Protocol

from identity.models import CustomUser


class IUserRepository(Protocol):
    """Persistence interface for CustomUser aggregates."""

    def get_by_id(self, user_id: int) -> CustomUser: ...
    def get_by_email(self, email: str) -> CustomUser: ...
    def save(self, user: CustomUser) -> CustomUser: ...
