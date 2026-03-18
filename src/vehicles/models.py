from django.db import models

from driver_profiles.models import DriverProfile


class Vehicle(models.Model):
    class Meta:
        verbose_name_plural = "Vehicles"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "license_plate",
                    "license_plate_state",
                ],
                name="unique_license_plate_state",
            )
        ]

    color = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    driver_profile = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    make = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    license_plate = models.CharField(max_length=9, blank=True)
    license_plate_state = models.CharField(max_length=2, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    vin = models.CharField(max_length=17)
    year = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.color} {self.year} {self.make} {self.model}"
