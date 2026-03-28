# DRF serializers for the identity bounded context.
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from identity.application.use_cases import RegisterUser


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    given_names = serializers.CharField()
    surnames = serializers.CharField()

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return RegisterUser().execute(**validated_data)
