import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activity", "0001_initial"),
        ("fleet", "0007_rename_vehicle_driver_profile_to_driver"),
    ]

    operations = [
        migrations.AddField(
            model_name="activityentry",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="activity_entries",
                to="fleet.vehicle",
            ),
            preserve_default=False,
        ),
        migrations.RemoveConstraint(
            model_name="activityentry",
            name="unique_driver_platform_date",
        ),
        migrations.AddConstraint(
            model_name="activityentry",
            constraint=models.UniqueConstraint(
                fields=("vehicle", "platform", "date"),
                name="unique_vehicle_platform_date",
            ),
        ),
    ]
