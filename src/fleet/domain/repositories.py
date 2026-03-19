"""Repository interfaces for the fleet bounded context.

These Protocol classes define the persistence contract that the domain
and application layers depend on. Application code imports only these
interfaces; the concrete Django ORM implementations live in
fleet.infrastructure.repositories and are injected at runtime.

This inversion keeps the domain free of ORM and database concerns.
"""

from typing import Protocol

from fleet.models import Driver, Vehicle


class IDriverRepository(Protocol):
    """Persistence interface for Driver aggregates."""

    def get_by_id(self, driver_id: int) -> Driver: ...
    def get_by_user_id(self, user_id: int) -> Driver: ...
    def save(self, driver: Driver) -> Driver: ...


class IVehicleRepository(Protocol):
    """Persistence interface for Vehicle entities."""

    def get_by_id(self, vehicle_id: int) -> Vehicle: ...
    def get_by_driver(self, driver: Driver) -> list[Vehicle]: ...
    def save(self, vehicle: Vehicle) -> Vehicle: ...
