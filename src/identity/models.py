from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from identity.infrastructure.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Platform user account.

    Email is used as the login identifier instead of a username.
    Names are stored as given_names (first/middle) and surnames
    (family names) to better support international name formats.
    """

    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(_("email address"), unique=True)
    given_names = models.CharField(_("given names"), max_length=64)
    is_active = models.BooleanField(_("is active"), default=True)
    is_staff = models.BooleanField(_("is staff"), default=False)
    surnames = models.CharField(_("surnames"), max_length=64)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.surnames}, {self.given_names} - {self.email}"
