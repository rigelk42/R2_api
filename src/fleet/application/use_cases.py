"""Application use cases for the fleet bounded context.

Each use case class orchestrates domain logic and persistence
without leaking infrastructure concerns into the domain.
"""

from fleet.models import Driver, Vehicle


class UpdateDriverProfile:
    """Update the driver's license information on a Driver profile."""

    def execute(self, driver: Driver, driver_license: str, driver_license_state: str):
        """Persist updated license fields for the given driver.

        Both fields must be supplied together (both non-empty or both blank).
        Validation of this invariant is performed at the serializer layer.

        Args:
            driver: The Driver instance to update.
            driver_license: License number, or an empty string to clear it.
            driver_license_state: Two-letter issuing state, or empty to clear.

        Returns:
            The updated Driver instance.
        """
        driver.driver_license = driver_license
        driver.driver_license_state = driver_license_state
        driver.save(update_fields=["driver_license", "driver_license_state"])

        return driver


class CreateVehicle:
    """Create and persist a new Vehicle for a driver."""

    def execute(
        self,
        driver: Driver,
        vin: str,
        year: int,
        make: str,
        model: str,
        color: str,
        license_plate: str,
        license_plate_state: str,
    ) -> Vehicle:
        """Instantiate and save a Vehicle with the provided attributes.

        Args:
            driver: The owning Driver.
            vin: 17-character Vehicle Identification Number (must be unique).
            year: Model year; must fall within the allowed rolling window.
            make: Manufacturer name (e.g. "Toyota").
            model: Model name (e.g. "Camry").
            color: Vehicle color.
            license_plate: Plate number, or empty string if not provided.
            license_plate_state: Two-letter issuing state, or empty string.

        Returns:
            The newly created Vehicle instance.
        """
        vehicle = Vehicle(
            driver=driver,
            vin=vin,
            year=year,
            make=make,
            model=model,
            color=color,
            license_plate=license_plate,
            license_plate_state=license_plate_state,
        )

        vehicle.save()
        return vehicle


class UpdateVehicle:
    """Update all mutable fields of an existing Vehicle."""

    def execute(
        self,
        vehicle: Vehicle,
        vin: str,
        year: int,
        make: str,
        model: str,
        color: str,
        license_plate: str,
        license_plate_state: str,
    ) -> Vehicle:
        """Replace all editable fields on the vehicle and persist the change.

        Args:
            vehicle: The Vehicle instance to update.
            vin: New or unchanged VIN.
            year: New or unchanged model year.
            make: New or unchanged manufacturer.
            model: New or unchanged model name.
            color: New or unchanged color.
            license_plate: New plate number, or empty string to clear.
            license_plate_state: New issuing state, or empty string to clear.

        Returns:
            The updated Vehicle instance.
        """
        vehicle.vin = vin
        vehicle.year = year
        vehicle.make = make
        vehicle.model = model
        vehicle.color = color
        vehicle.license_plate = license_plate
        vehicle.license_plate_state = license_plate_state
        vehicle.save(
            update_fields=[
                "vin",
                "year",
                "make",
                "model",
                "color",
                "license_plate",
                "license_plate_state",
            ]
        )

        return vehicle


class DeleteVehicle:
    """Delete a Vehicle and its associated activity entries (via CASCADE)."""

    def execute(self, vehicle: Vehicle) -> None:
        """Remove the vehicle from the database.

        Cascades to any ActivityEntry rows linked to this vehicle.

        Args:
            vehicle: The Vehicle instance to delete.
        """
        vehicle.delete()
