import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from drivers.models import Driver


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
    driver_profile = models.ForeignKey(
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
