"""DRF serializers for the fleet bounded context."""

from rest_framework import serializers

from fleet.application.use_cases import UpdateDriverProfile


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
