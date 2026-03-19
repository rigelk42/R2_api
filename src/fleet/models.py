import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Driver(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["driver_license", "driver_license_state"],
                condition=models.Q(driver_license__gt=""),
                name="unique_driver_license_state",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(driver_license="", driver_license_state="")
                    | (
                        ~models.Q(driver_license="")
                        & ~models.Q(driver_license_state="")
                    )
                ),
                name="driver_license_both_or_neither",
            ),
        ]

    created_at = models.DateTimeField(auto_now_add=True)
    driver_license = models.CharField(max_length=16, blank=True)
    driver_license_state = models.CharField(max_length=2, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_profile",
    )

    def __str__(self) -> str:
        return str(self.user)


class Vehicle(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["license_plate", "license_plate_state"],
                condition=models.Q(license_plate__gt=""),
                name="unique_license_plate_state",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(license_plate="", license_plate_state="")
                    | (~models.Q(license_plate="") & ~models.Q(license_plate_state=""))
                ),
                name="license_plate_both_or_neither",
            ),
        ]

    color = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="vehicles"
    )
    make = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    license_plate = models.CharField(max_length=9, blank=True)
    license_plate_state = models.CharField(max_length=2, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    vin = models.CharField(max_length=17, unique=True)
    year = models.IntegerField(
        validators=[
            MinValueValidator(datetime.date.today().year - 15),
            MaxValueValidator(datetime.date.today().year + 1),
        ]
    )

    def __str__(self) -> str:
        return f"{self.color} {self.year} {self.make} {self.model}"
