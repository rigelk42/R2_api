"""DRF serializers for the activity bounded context."""

from rest_framework import serializers

from activity.application.use_cases import (
    CreateActivityEntry,
    CreateExpenseEntry,
    CreateMileageEntry,
    UpdateActivityEntry,
    UpdateExpenseEntry,
    UpdateMileageEntry,
)
from activity.models import ExpenseCategory, MileageEntry, Platform


class PlatformSerializer(serializers.Serializer):
    """Read-only serializer for displaying platform data in API responses."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.SlugField(read_only=True)


class ActivityEntrySerializer(serializers.Serializer):
    """Read-only serializer for displaying activity entry data in API responses."""

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
    """Validates and processes activity entry create/update input.

    Enforces that the referenced vehicle belongs to the requesting driver
    and that active_time does not exceed online_time. Delegates persistence
    to CreateActivityEntry or UpdateActivityEntry depending on context.
    """

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
        """Ensure the vehicle belongs to the driver and active_time <= online_time."""
        driver = self.context["request"].user.driver_profile

        if not driver.vehicles.filter(pk=data["vehicle_id"]).exists():
            raise serializers.ValidationError({"vehicle_id": "Vehicle not found."})
        if data["active_time"] > data["online_time"]:
            raise serializers.ValidationError(
                {"active_time": "Active time cannot exceed online time."}
            )

        return data

    def create(self, validated_data):
        """Invoke CreateActivityEntry for the authenticated driver."""
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
        """Invoke UpdateActivityEntry on the existing activity entry instance."""
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
    """Read-only serializer for displaying mileage entry data in API responses."""

    id = serializers.IntegerField(read_only=True)
    month = serializers.CharField(read_only=True)
    miles = serializers.DecimalField(max_digits=8, decimal_places=1, read_only=True)
    deduction = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)


class MileageEntryWriteSerializer(serializers.Serializer):
    """Validates and processes mileage entry create/update input.

    Enforces that only one entry exists per driver per month and delegates
    persistence to CreateMileageEntry or UpdateMileageEntry.
    """

    month = serializers.RegexField(r"^\d{4}-\d{2}$")
    miles = serializers.DecimalField(max_digits=8, decimal_places=1)
    deduction = serializers.DecimalField(max_digits=8, decimal_places=2)

    def validate(self, data):
        """Ensure no other mileage entry exists for this driver and month."""
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
        """Invoke CreateMileageEntry for the authenticated driver."""
        driver = self.context["request"].user.driver_profile
        return CreateMileageEntry().execute(
            driver=driver,
            month=validated_data["month"],
            miles=validated_data["miles"],
            deduction=validated_data["deduction"],
        )

    def update(self, instance, validated_data):
        """Invoke UpdateMileageEntry on the existing mileage entry instance."""
        return UpdateMileageEntry().execute(
            entry=instance,
            month=validated_data["month"],
            miles=validated_data["miles"],
            deduction=validated_data["deduction"],
        )


class ExpenseEntrySerializer(serializers.Serializer):
    """Read-only serializer for displaying expense entry data in API responses."""

    id = serializers.IntegerField(read_only=True)
    vehicle_id = serializers.IntegerField(read_only=True)
    date = serializers.DateField(read_only=True)
    vendor = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    category_display = serializers.SerializerMethodField()
    amount = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    def get_category_display(self, obj):
        """Return the human-readable label for the expense category."""
        return obj.get_category_display()


class ExpenseEntryWriteSerializer(serializers.Serializer):
    """Validates and processes expense entry create/update input.

    Enforces that the referenced vehicle belongs to the requesting driver.
    Delegates persistence to CreateExpenseEntry or UpdateExpenseEntry.
    """

    vehicle_id = serializers.IntegerField()
    date = serializers.DateField()
    vendor = serializers.CharField(max_length=128)
    category = serializers.ChoiceField(choices=ExpenseCategory.choices)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)

    def validate(self, data):
        """Ensure the vehicle belongs to the authenticated driver."""
        driver = self.context["request"].user.driver_profile
        if not driver.vehicles.filter(pk=data["vehicle_id"]).exists():
            raise serializers.ValidationError({"vehicle_id": "Vehicle not found."})
        return data

    def create(self, validated_data):
        """Invoke CreateExpenseEntry for the authenticated driver."""
        driver = self.context["request"].user.driver_profile
        vehicle = driver.vehicles.get(pk=validated_data["vehicle_id"])
        return CreateExpenseEntry().execute(
            driver=driver,
            vehicle=vehicle,
            date=validated_data["date"],
            vendor=validated_data["vendor"],
            category=validated_data["category"],
            amount=validated_data["amount"],
        )

    def update(self, instance, validated_data):
        """Invoke UpdateExpenseEntry on the existing expense entry instance."""
        driver = self.context["request"].user.driver_profile
        vehicle = driver.vehicles.get(pk=validated_data["vehicle_id"])
        return UpdateExpenseEntry().execute(
            entry=instance,
            vehicle=vehicle,
            date=validated_data["date"],
            vendor=validated_data["vendor"],
            category=validated_data["category"],
            amount=validated_data["amount"],
        )
