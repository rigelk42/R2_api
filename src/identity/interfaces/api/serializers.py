"""DRF serializers for the identity bounded context."""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from identity.application.use_cases import RegisterUser, UpdateUser


class SignupSerializer(serializers.Serializer):
    """Validates and processes user registration input.

    On successful validation, delegates to RegisterUser to create
    the account and its associated driver profile.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    given_names = serializers.CharField()
    surnames = serializers.CharField()

    def validate_password(self, value):
        """Run Django's built-in password validators against the candidate password."""
        validate_password(value)
        return value

    def create(self, validated_data):
        """Invoke the RegisterUser use case with the validated field values."""
        return RegisterUser().execute(**validated_data)


class UpdateUserSerializer(serializers.Serializer):
    """Validates and processes profile update input for an existing user.

    Email is exposed as read-only for display purposes and cannot be
    changed through this serializer. Delegates persistence to UpdateUser.
    """

    email = serializers.EmailField(read_only=True)
    given_names = serializers.CharField()
    surnames = serializers.CharField()

    def update(self, instance, validated_data):
        """Invoke the UpdateUser use case with the validated field values."""
        return UpdateUser().execute(instance, **validated_data)
