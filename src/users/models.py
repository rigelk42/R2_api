from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "Custom Users"

    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(_("Email Address"), unique=True)
    given_names = models.CharField(_("Given Names"), max_length=32)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    surnames = models.CharField(_("Surnames"), max_length=32)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.surnames}, {self.given_names} - {self.email}"
