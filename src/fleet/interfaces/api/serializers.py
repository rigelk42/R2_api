"""DRF serializers for the fleet bounded context."""

from rest_framework import serializers

from fleet.application.use_cases import (
    CreateVehicle,
    UpdateDriverProfile,
    UpdateVehicle,
)


class DriverProfileSerializer(serializers.Serializer):
    """Validates and processes driver profile updates.

    Enforces the both-or-neither rule for driver license fields and
    delegates persistence to UpdateDriverProfile.
    """

    driver_license = serializers.CharField(allow_blank=True)
    driver_license_state = serializers.CharField(allow_blank=True)

    def validate(self, data):
        """Ensure license number and state are provided together or not at all."""
        if bool(data.get("driver_license")) != bool(data.get("driver_license_state")):
            raise serializers.ValidationError(
                "Driver license and license state must both be provided or both empty"
            )

        return data

    def update(self, instance, validated_data):
        """Invoke UpdateDriverProfile with the validated license fields."""
        return UpdateDriverProfile().execute(instance, **validated_data)


class VehicleSerializer(serializers.Serializer):
    """Read-only serializer for displaying vehicle data in API responses."""

    id = serializers.IntegerField(read_only=True)
    vin = serializers.CharField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    make = serializers.CharField(read_only=True)
    model = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)
    license_plate = serializers.CharField(read_only=True)
    license_plate_state = serializers.CharField(read_only=True)


class VehicleWriteSerializer(serializers.Serializer):
    """Validates and processes vehicle create/update input.

    Enforces the both-or-neither rule for license plate fields and
    delegates to CreateVehicle or UpdateVehicle depending on context.
    """

    vin = serializers.CharField()
    year = serializers.IntegerField()
    make = serializers.CharField()
    model = serializers.CharField()
    color = serializers.CharField()
    license_plate = serializers.CharField(allow_blank=True)
    license_plate_state = serializers.CharField(allow_blank=True)

    def validate(self, data):
        """Ensure license plate and state are provided together or not at all."""
        if bool(data.get("license_plate")) != bool(data.get("license_plate_state")):
            raise serializers.ValidationError(
                "License plate and plate state must both be provided or both empty"
            )

        return data

    def create(self, validated_data):
        """Invoke CreateVehicle for the authenticated driver."""
        driver = self.context["request"].user.driver_profile
        return CreateVehicle().execute(driver, **validated_data)

    def update(self, instance, validated_data):
        """Invoke UpdateVehicle on the existing vehicle instance."""
        return UpdateVehicle().execute(instance, **validated_data)
