"""Application use cases for the fleet bounded context.

Each use case class orchestrates domain logic and persistence
without leaking infrastructure concerns into the domain.
"""

from fleet.models import Driver, Vehicle


class UpdateDriverProfile:
    def execute(self, driver: Driver, driver_license: str, driver_license_state: str):
        driver.driver_license = driver_license
        driver.driver_license_state = driver_license_state
        driver.save(update_fields=["driver_license", "driver_license_state"])

        return driver


class CreateVehicle:
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
    ):
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
    def execute(self, vehicle: Vehicle):
        vehicle.delete()
