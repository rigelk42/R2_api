"""Repository interfaces for the activity bounded context.

These Protocol classes define the persistence contract that the domain
and application layers depend on. The concrete Django ORM implementations
live in activity.infrastructure.repositories and are injected at runtime.
"""

import datetime
from typing import Protocol

from activity.models import ActivityEntry, Platform


class IPlatformRepository(Protocol):
    """Persistence interface for Platform reference data."""

    def get_by_id(self, platform_id: int) -> Platform: ...
    def get_by_slug(self, slug: str) -> Platform: ...
    def list_all(self) -> list[Platform]: ...


class IActivityEntryRepository(Protocol):
    """Persistence interface for ActivityEntry aggregates."""

    def get_by_id(self, entry_id: int) -> ActivityEntry: ...
    def get_by_driver(self, driver_id: int) -> list[ActivityEntry]: ...
    def get_by_driver_and_date_range(
        self,
        driver_id: int,
        start: datetime.date,
        end: datetime.date,
    ) -> list[ActivityEntry]: ...
    def save(self, entry: ActivityEntry) -> ActivityEntry: ...
    def delete(self, entry: ActivityEntry) -> None: ...
