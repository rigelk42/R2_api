"""Django ORM implementations of the activity repository interfaces.

These classes satisfy the contracts defined in activity.domain.repositories
using Django's ORM. They are the only place in the activity bounded context
that issues database queries directly.
"""

import datetime

from activity.models import ActivityEntry, MileageEntry, Platform


class PlatformRepository:
    """IPlatformRepository backed by the Django ORM."""

    def get_by_id(self, platform_id: int) -> Platform:
        return Platform.objects.get(pk=platform_id)

    def get_by_slug(self, slug: str) -> Platform:
        return Platform.objects.get(slug=slug)

    def list_all(self) -> list[Platform]:
        return list(Platform.objects.all())


class ActivityEntryRepository:
    """IActivityEntryRepository backed by the Django ORM."""

    def get_by_id(self, entry_id: int) -> ActivityEntry:
        return ActivityEntry.objects.get(pk=entry_id)

    def get_by_driver(self, driver_id: int) -> list[ActivityEntry]:
        return list(ActivityEntry.objects.filter(driver_id=driver_id))

    def get_by_driver_and_date_range(
        self,
        driver_id: int,
        start: datetime.date,
        end: datetime.date,
    ) -> list[ActivityEntry]:
        return list(
            ActivityEntry.objects.filter(
                driver_id=driver_id,
                date__gte=start,
                date__lte=end,
            )
        )

    def get_by_vehicle(self, vehicle_id: int) -> list[ActivityEntry]:
        return list(ActivityEntry.objects.filter(vehicle_id=vehicle_id))

    def save(self, entry: ActivityEntry) -> ActivityEntry:
        entry.save()
        return entry

    def delete(self, entry: ActivityEntry) -> None:
        entry.delete()


class MileageEntryRepository:
    """IMileageEntryRepository backed by the Django ORM."""

    def get_by_id(self, entry_id: int) -> MileageEntry:
        return MileageEntry.objects.get(pk=entry_id)

    def get_by_driver(self, driver_id: int) -> list[MileageEntry]:
        return list(MileageEntry.objects.filter(driver_id=driver_id))

    def get_by_driver_and_month(self, driver_id: int, month: str) -> list[MileageEntry]:
        return list(MileageEntry.objects.filter(driver_id=driver_id, month=month))

    def save(self, entry: MileageEntry) -> MileageEntry:
        entry.save()
        return entry

    def delete(self, entry: MileageEntry) -> None:
        entry.delete()
