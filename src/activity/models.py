from decimal import Decimal

from django.db import models


class Platform(models.Model):
    """A rideshare platform such as Uber or Lyft.

    Platforms are seeded as reference data and are not created by end
    users. The slug is the stable internal identifier (e.g. "uber",
    "lyft") used in code and APIs; name is the human-readable label.
    """

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class ActivityEntry(models.Model):
    """A single day's driving activity logged on one rideshare platform.

    Captures the time a driver spent online (logged in and available)
    versus active (on a trip), along with base income and tips earned.
    Only one entry is allowed per vehicle per platform per day.

    Both driver and vehicle are stored directly for query convenience;
    the vehicle must belong to the driver (enforced at the application
    layer). The vehicle FK cascades on deletion so entries are removed
    when the vehicle is removed from the system.

    Time fields use DurationField, which accepts HH:MM:SS input and
    maps to a PostgreSQL interval column. Active time must not exceed
    online time, enforced both here and at the database level.

    Currency amounts are in USD. Tips default to zero; income is always
    required since a sessionless entry has no meaning.
    """

    driver = models.ForeignKey(
        "fleet.Driver",
        on_delete=models.CASCADE,
        related_name="activity_entries",
    )
    vehicle = models.ForeignKey(
        "fleet.Vehicle",
        on_delete=models.CASCADE,
        related_name="activity_entries",
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.PROTECT,
        related_name="entries",
    )
    date = models.DateField()
    online_time = models.DurationField(
        help_text="Total time logged in on the platform (HH:MM:SS)."
    )
    active_time = models.DurationField(
        help_text="Total time spent on trips (HH:MM:SS). Must not exceed online time."
    )
    income = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Base pay earned, in USD.",
    )
    tips = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0"),
        help_text="Tips earned, in USD.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vehicle", "platform", "date"],
                name="unique_vehicle_platform_date",
            ),
            models.CheckConstraint(
                condition=models.Q(active_time__lte=models.F("online_time")),
                name="active_time_lte_online_time",
            ),
        ]

    def __str__(self) -> str:
        user = self.driver.user
        v = self.vehicle
        return (
            f"{user.surnames}, {user.given_names}"
            f" - {v.year} {v.make} {v.model}"
            f" - {self.platform}"
            f" - {self.date}"
        )
