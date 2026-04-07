"""DRF serializers for the activity bounded context."""

from rest_framework import serializers

from activity.application.use_cases import (CreateActivityEntry,
                                            CreateMileageEntry,
                                            UpdateActivityEntry,
                                            UpdateMileageEntry)
from activity.models import MileageEntry, Platform


class PlatformSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.SlugField(read_only=True)


class ActivityEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    vehicle_id = serializers.IntegerField(read_only=True)
    platform_id = serializers.IntegerField(read_only=True)
    platform_name = serializers.CharField(source="platform.name", read_only=True)
    platform_slug = serializers.SlugField(source="platform.slug", read_only=True)
    date = serializers.DateField(read_only=True)
    online_time = serializers.DurationField(read_only=True)
    active_time = serializers.DurationField(read_only=True)
    income = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    tips = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)


class ActivityEntryWriteSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()
    platform_id = serializers.IntegerField()
    date = serializers.DateField()
    online_time = serializers.DurationField()
    active_time = serializers.DurationField()
    income = serializers.DecimalField(max_digits=8, decimal_places=2)
    tips = serializers.DecimalField(
        max_digits=8, decimal_places=2, required=False, default=0
    )

    def validate(self, data):
        driver = self.context["request"].user.driver_profile

        if not driver.vehicles.filter(pk=data["vehicle_id"]).exists():
            raise serializers.ValidationError({"vehicle_id": "Vehicle not found."})
        if data["active_time"] > data["online_time"]:
            raise serializers.ValidationError(
                {"active_time": "Active time cannot exceed online time."}
            )

        return data

    def create(self, validated_data):
        driver = self.context["request"].user.driver_profile
        vehicle = driver.vehicles.get(pk=validated_data["vehicle_id"])
        platform = Platform.objects.get(pk=validated_data["platform_id"])

        return CreateActivityEntry().execute(
            driver=driver,
            vehicle=vehicle,
            platform=platform,
            date=validated_data["date"],
            online_time=validated_data["online_time"],
            active_time=validated_data["active_time"],
            income=validated_data["income"],
            tips=validated_data["tips"],
        )

    def update(self, instance, validated_data):
        driver = self.context["request"].user.driver_profile
        vehicle = driver.vehicles.get(pk=validated_data["vehicle_id"])
        platform = Platform.objects.get(pk=validated_data["platform_id"])

        return UpdateActivityEntry().execute(
            activity_entry=instance,
            vehicle=vehicle,
            platform=platform,
            date=validated_data["date"],
            online_time=validated_data["online_time"],
            active_time=validated_data["active_time"],
            income=validated_data["income"],
            tips=validated_data["tips"],
        )


class MileageEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    month = serializers.CharField(read_only=True)
    miles = serializers.DecimalField(max_digits=8, decimal_places=1, read_only=True)
    deduction = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)


class MileageEntryWriteSerializer(serializers.Serializer):
    month = serializers.RegexField(r"^\d{4}-\d{2}$")
    miles = serializers.DecimalField(max_digits=8, decimal_places=1)
    deduction = serializers.DecimalField(max_digits=8, decimal_places=2)

    def validate(self, data):
        driver = self.context["request"].user.driver_profile
        qs = MileageEntry.objects.filter(driver=driver, month=data["month"])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                {"month": "A mileage entry for this month already exists."}
            )
        return data

    def create(self, validated_data):
        driver = self.context["request"].user.driver_profile
        return CreateMileageEntry().execute(
            driver=driver,
            month=validated_data["month"],
            miles=validated_data["miles"],
            deduction=validated_data["deduction"],
        )

    def update(self, instance, validated_data):
        return UpdateMileageEntry().execute(
            entry=instance,
            month=validated_data["month"],
            miles=validated_data["miles"],
            deduction=validated_data["deduction"],
        )
