from django.db import models

from users.models import CustomUser


class DriverProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    driver_license = models.CharField(max_length=16, blank=True)
    driver_license_state = models.CharField(max_length=2, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}, "
