"""DRF serializers for the fleet bounded context."""

from rest_framework import serializers

from fleet.application.use_cases import (CreateVehicle, UpdateDriverProfile,
                                         UpdateVehicle)


class DriverProfileSerializer(serializers.Serializer):
    driver_license = serializers.CharField(allow_blank=True)
    driver_license_state = serializers.CharField(allow_blank=True)

    def validate(self, data):
        if bool(data.get("driver_license")) != bool(data.get("driver_license_state")):
            raise serializers.ValidationError(
                "Driver license and driver license state must both be provided or both empty"
            )

        return data

    def update(self, instance, validated_data):
        return UpdateDriverProfile().execute(instance, **validated_data)


class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    vin = serializers.CharField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    make = serializers.CharField(read_only=True)
    model = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)
    license_plate = serializers.CharField(read_only=True)
    license_plate_state = serializers.CharField(read_only=True)


class VehicleWriteSerializer(serializers.Serializer):
    vin = serializers.CharField()
    year = serializers.IntegerField()
    make = serializers.CharField()
    model = serializers.CharField()
    color = serializers.CharField()
    license_plate = serializers.CharField(allow_blank=True)
    license_plate_state = serializers.CharField(allow_blank=True)

    def validate(self, data):
        if bool(data.get("license_plate")) != bool(data.get("license_plate_state")):
            raise serializers.ValidationError(
                "License plate and license plate state must both be provided or both empty"
            )

        return data

    def create(self, validated_data):
        driver = self.context["request"].user.driver_profile
        return CreateVehicle().execute(driver, **validated_data)

    def update(self, instance, validated_data):
        return UpdateVehicle().execute(instance, **validated_data)
