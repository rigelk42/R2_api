from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from identity.infrastructure.forms import (CustomUserChangeForm,
                                           CustomUserCreationForm)
from identity.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Django admin configuration for CustomUser.

    Replaces the default username-centric layout with email-based
    authentication fields and surfaces given_names/surnames throughout
    the list view, search, and edit forms.
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "surnames",
        "given_names",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "surnames", "given_names", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "surnames",
                    "given_names",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
