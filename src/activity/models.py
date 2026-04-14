from decimal import Decimal

from django.db import models


class ExpenseCategory(models.TextChoices):
    """Fixed set of rideshare-related expense categories.

    Used as the choices argument on ExpenseEntry.category. The left-hand
    value (e.g. "gasoline") is stored in the database; the right-hand
    string (e.g. "Gasoline") is the human-readable display label returned
    by get_category_display().
    """

    GASOLINE = "gasoline", "Gasoline"
    VEHICLE_MAINTENANCE = "vehicle_maintenance", "Vehicle Maintenance"
    PARKING = "parking", "Parking"
    TOLLS = "tolls", "Tolls"
    CAR_WASH = "car_wash", "Car Wash / Detailing"
    PHONE_DATA = "phone_data", "Phone & Data"
    INSURANCE = "insurance", "Insurance"
    REGISTRATION = "registration", "Registration & Licensing"
    ACCESSORIES = "accessories", "Accessories"
    OTHER = "other", "Other"


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


class MileageEntry(models.Model):
    """Monthly mileage log for a driver.

    Records the total miles driven in a given month and the corresponding
    tax deduction amount in USD. Only one entry is allowed per driver per
    month (enforced by the unique constraint on driver + month).

    The month field stores a YYYY-MM string (e.g. "2025-01") to avoid
    ambiguity when storing a partial date.
    """

    driver = models.ForeignKey(
        "fleet.Driver",
        on_delete=models.CASCADE,
        related_name="mileage_entries",
    )
    month = models.CharField(
        max_length=7,
        help_text="Month this entry covers, in YYYY-MM format.",
    )
    miles = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        help_text="Total miles driven during the month.",
    )
    deduction = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Tax deduction amount for the miles driven, in USD.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["driver", "month"],
                name="unique_driver_month_mileage",
            ),
        ]

    def __str__(self) -> str:
        user = self.driver.user
        return f"{user.surnames}, {user.given_names} - {self.month}"


class ExpenseEntry(models.Model):
    """A single out-of-pocket expense incurred while operating as a driver.

    Captures the date, vendor, category, and amount of an expense. Category
    is a fixed set of choices (see ExpenseCategory) covering the most common
    rideshare-related costs. Only one instance of this model has no uniqueness
    constraint across fields — a driver may have multiple expenses of the same
    category on the same day (e.g. two toll charges).

    Currency amounts are in USD.
    """

    driver = models.ForeignKey(
        "fleet.Driver",
        on_delete=models.CASCADE,
        related_name="expense_entries",
    )
    vehicle = models.ForeignKey(
        "fleet.Vehicle",
        on_delete=models.CASCADE,
        related_name="expense_entries",
    )
    date = models.DateField(help_text="Date the expense was incurred.")
    vendor = models.CharField(
        max_length=128,
        help_text="Name of the vendor or payee.",
    )
    category = models.CharField(
        max_length=32,
        choices=ExpenseCategory.choices,
        help_text="Expense category.",
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Amount paid, in USD.",
    )

    def __str__(self) -> str:
        user = self.driver.user
        return (
            f"{user.surnames}, {user.given_names}"
            f" - {self.get_category_display()}"
            f" - {self.date}"
        )
