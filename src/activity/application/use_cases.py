"""Application use cases for the activity bounded context.

Each use case class orchestrates domain logic and persistence
without leaking infrastructure concerns into the domain.
"""

from activity.models import ActivityEntry, MileageEntry


class CreateActivityEntry:
    def execute(
        self, driver, vehicle, platform, date, online_time, active_time, income, tips
    ) -> ActivityEntry:
        activity_entry = ActivityEntry(
            driver=driver,
            vehicle=vehicle,
            platform=platform,
            date=date,
            online_time=online_time,
            active_time=active_time,
            income=income,
            tips=tips,
        )

        activity_entry.save()
        return activity_entry


class UpdateActivityEntry:
    def execute(
        self,
        activity_entry,
        vehicle,
        platform,
        date,
        online_time,
        active_time,
        income,
        tips,
    ) -> ActivityEntry:
        activity_entry.vehicle = vehicle
        activity_entry.platform = platform
        activity_entry.date = date
        activity_entry.online_time = online_time
        activity_entry.active_time = active_time
        activity_entry.income = income
        activity_entry.tips = tips

        activity_entry.save(
            update_fields=[
                "vehicle",
                "platform",
                "date",
                "online_time",
                "active_time",
                "income",
                "tips",
            ]
        )

        return activity_entry


class DeleteActivityEntry:
    def execute(self, activity_entry: ActivityEntry):
        activity_entry.delete()


class CreateMileageEntry:
    def execute(self, driver, month: str, miles, deduction) -> MileageEntry:
        entry = MileageEntry(
            driver=driver, month=month, miles=miles, deduction=deduction
        )
        entry.save()
        return entry


class UpdateMileageEntry:
    def execute(
        self, entry: MileageEntry, month: str, miles, deduction
    ) -> MileageEntry:
        entry.month = month
        entry.miles = miles
        entry.deduction = deduction
        entry.save(update_fields=["month", "miles", "deduction"])
        return entry


class DeleteMileageEntry:
    def execute(self, entry: MileageEntry) -> None:
        entry.delete()
