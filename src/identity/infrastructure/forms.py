from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from identity.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Admin form for creating a new CustomUser.

    Replaces the default username field with email and exposes
    given_names/surnames instead of a single name field.
    """

    class Meta:
        model = CustomUser
        fields = ("email", "surnames", "given_names")


class CustomUserChangeForm(UserChangeForm):
    """Admin form for editing an existing CustomUser.

    Mirrors CustomUserCreationForm's field selection so the admin
    experience is consistent between create and edit workflows.
    """

    class Meta:
        model = CustomUser
        fields = ("email", "surnames", "given_names")
