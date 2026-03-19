"""Django ORM implementations of the fleet repository interfaces.

These classes satisfy the contracts defined in fleet.domain.repositories
using Django's ORM. They are the only place in the fleet bounded context
that issues database queries directly.
"""

from fleet.models import Driver, Vehicle


class DjangoDriverRepository:
    """IDriverRepository backed by the Django ORM."""

    def get_by_id(self, driver_id: int) -> Driver:
        return Driver.objects.get(pk=driver_id)

    def get_by_user_id(self, user_id: int) -> Driver:
        return Driver.objects.get(user_id=user_id)

    def save(self, driver: Driver) -> Driver:
        driver.save()
        return driver


class DjangoVehicleRepository:
    """IVehicleRepository backed by the Django ORM."""

    def get_by_id(self, vehicle_id: int) -> Vehicle:
        return Vehicle.objects.get(pk=vehicle_id)

    def get_by_driver(self, driver: Driver) -> list[Vehicle]:
        return list(Vehicle.objects.filter(driver=driver))

    def save(self, vehicle: Vehicle) -> Vehicle:
        vehicle.save()
        return vehicle
