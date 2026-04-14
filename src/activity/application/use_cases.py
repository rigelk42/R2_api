"""Application use cases for the activity bounded context.

Each use case class orchestrates domain logic and persistence
without leaking infrastructure concerns into the domain.
"""

from activity.models import ActivityEntry, ExpenseEntry, MileageEntry


class CreateActivityEntry:
    """Create and persist a new ActivityEntry for a driver."""

    def execute(
        self, driver, vehicle, platform, date, online_time, active_time, income, tips
    ) -> ActivityEntry:
        """Instantiate and save an ActivityEntry with the provided attributes.

        Args:
            driver: The owning Driver.
            vehicle: The Vehicle used during this session.
            platform: The rideshare Platform (e.g. Uber, Lyft).
            date: The calendar date of the activity.
            online_time: Total time logged in on the platform.
            active_time: Total time spent on trips; must not exceed online_time.
            income: Base pay earned, in USD.
            tips: Tips earned, in USD.

        Returns:
            The newly created ActivityEntry instance.
        """
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
    """Update all mutable fields of an existing ActivityEntry."""

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
        """Replace all editable fields on the entry and persist the change.

        Args:
            activity_entry: The ActivityEntry instance to update.
            vehicle: New or unchanged vehicle.
            platform: New or unchanged platform.
            date: New or unchanged activity date.
            online_time: New or unchanged total logged-in time.
            active_time: New or unchanged total on-trip time.
            income: New or unchanged base pay, in USD.
            tips: New or unchanged tips, in USD.

        Returns:
            The updated ActivityEntry instance.
        """
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
    """Delete an ActivityEntry from the database."""

    def execute(self, activity_entry: ActivityEntry) -> None:
        """Remove the activity entry.

        Args:
            activity_entry: The ActivityEntry instance to delete.
        """
        activity_entry.delete()


class CreateMileageEntry:
    """Create and persist a new MileageEntry for a driver."""

    def execute(self, driver, month: str, miles, deduction) -> MileageEntry:
        """Instantiate and save a MileageEntry with the provided attributes.

        Args:
            driver: The owning Driver.
            month: The month covered by this entry, in YYYY-MM format.
            miles: Total miles driven during the month.
            deduction: Tax deduction amount for the miles driven, in USD.

        Returns:
            The newly created MileageEntry instance.
        """
        entry = MileageEntry(
            driver=driver, month=month, miles=miles, deduction=deduction
        )
        entry.save()
        return entry


class UpdateMileageEntry:
    """Update all mutable fields of an existing MileageEntry."""

    def execute(
        self, entry: MileageEntry, month: str, miles, deduction
    ) -> MileageEntry:
        """Replace all editable fields on the mileage entry and persist the change.

        Args:
            entry: The MileageEntry instance to update.
            month: New or unchanged month, in YYYY-MM format.
            miles: New or unchanged total miles driven.
            deduction: New or unchanged tax deduction amount, in USD.

        Returns:
            The updated MileageEntry instance.
        """
        entry.month = month
        entry.miles = miles
        entry.deduction = deduction
        entry.save(update_fields=["month", "miles", "deduction"])
        return entry


class DeleteMileageEntry:
    """Delete a MileageEntry from the database."""

    def execute(self, entry: MileageEntry) -> None:
        """Remove the mileage entry.

        Args:
            entry: The MileageEntry instance to delete.
        """
        entry.delete()


class CreateExpenseEntry:
    """Create and persist a new ExpenseEntry for a driver."""

    def execute(
        self, driver, vehicle, date, vendor: str, category: str, amount
    ) -> ExpenseEntry:
        """Instantiate and save an ExpenseEntry with the provided attributes.

        Args:
            driver: The owning Driver.
            vehicle: The Vehicle the expense is associated with.
            date: The date the expense was incurred.
            vendor: Name of the vendor or payee.
            category: Expense category slug (see ExpenseCategory).
            amount: Amount paid, in USD.

        Returns:
            The newly created ExpenseEntry instance.
        """
        entry = ExpenseEntry(
            driver=driver,
            vehicle=vehicle,
            date=date,
            vendor=vendor,
            category=category,
            amount=amount,
        )
        entry.save()
        return entry


class UpdateExpenseEntry:
    """Update all mutable fields of an existing ExpenseEntry."""

    def execute(
        self, entry: ExpenseEntry, vehicle, date, vendor: str, category: str, amount
    ) -> ExpenseEntry:
        """Replace all editable fields on the expense entry and persist the change.

        Args:
            entry: The ExpenseEntry instance to update.
            vehicle: New or unchanged vehicle.
            date: New or unchanged expense date.
            vendor: New or unchanged vendor name.
            category: New or unchanged category slug.
            amount: New or unchanged amount paid, in USD.

        Returns:
            The updated ExpenseEntry instance.
        """
        entry.vehicle = vehicle
        entry.date = date
        entry.vendor = vendor
        entry.category = category
        entry.amount = amount
        entry.save(update_fields=["vehicle", "date", "vendor", "category", "amount"])
        return entry


class DeleteExpenseEntry:
    """Delete an ExpenseEntry from the database."""

    def execute(self, entry: ExpenseEntry) -> None:
        """Remove the expense entry.

        Args:
            entry: The ExpenseEntry instance to delete.
        """
        entry.delete()
