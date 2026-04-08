from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """Create, save, and return a regular (non-staff) user.

        Args:
            email: The user's email address; used as the login identifier.
            password: Plain-text password; hashed before storage.
            **extra_fields: Additional model fields (e.g. given_names, surnames).

        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create, save, and return a superuser with all permissions.

        Defaults is_staff, is_superuser, and is_active to True. Raises
        if the caller explicitly passes False for either permission flag.

        Args:
            email: The superuser's email address.
            password: Plain-text password; hashed before storage.
            **extra_fields: Additional model fields.

        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
