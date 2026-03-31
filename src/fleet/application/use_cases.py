"""Application use cases for the fleet bounded context.

Each use case class orchestrates domain logic and persistence
without leaking infrastructure concerns into the domain.
"""

from fleet.models import Driver


class UpdateDriverProfile:
    def execute(self, driver: Driver, driver_license: str, driver_license_state: str):
        driver.driver_license = driver_license
        driver.driver_license_state = driver_license_state
        driver.save(update_fields=["driver_license", "driver_license_state"])

        return driver
