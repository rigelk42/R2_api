"""Value objects for the fleet bounded context.

Value objects are immutable and defined entirely by their attributes.
Two instances with the same attributes are equal. Each class enforces
its own invariants in __post_init__, making invalid states unrepresentable.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DriverLicense:
    """A driver's license identified by number and issuing state.

    Both fields must be non-empty; a partial license (number without
    state, or vice versa) is not a valid domain concept.
    """

    number: str
    state: str

    def __post_init__(self):
        if bool(self.number) != bool(self.state):
            raise ValueError("Both license number and state must be provided together.")


@dataclass(frozen=True)
class LicensePlate:
    """A vehicle license plate identified by plate number and issuing state.

    Both fields must be non-empty; a partial plate is not valid.
    """

    plate: str
    state: str

    def __post_init__(self):
        if bool(self.plate) != bool(self.state):
            raise ValueError("Both license plate and state must be provided together.")


@dataclass(frozen=True)
class VehicleYear:
    """The model year of a vehicle.

    Accepted range: up to 15 years in the past through 1 year in the
    future relative to the current calendar year. This mirrors the
    validator range enforced on the Vehicle ORM model.
    """

    value: int

    def __post_init__(self):
        import datetime

        current_year = datetime.date.today().year
        if not (current_year - 15 <= self.value <= current_year + 1):
            raise ValueError(f"Vehicle year {self.value} is outside the allowed range.")
