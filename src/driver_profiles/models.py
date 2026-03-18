from django.db import models

from users.models import CustomUser


class DriverProfile(models.Model):
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
        CustomUser, on_delete=models.CASCADE, related_name="driver_profile"
    )

    def __str__(self) -> str:
        return str(self.user)
