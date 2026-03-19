from dataclasses import dataclass


@dataclass(frozen=True)
class DriverLicense:
    number: str
    state: str

    def __post_init__(self):
        if bool(self.number) != bool(self.state):
            raise ValueError("Both license number and state must be provided together.")


@dataclass(frozen=True)
class LicensePlate:
    plate: str
    state: str

    def __post_init__(self):
        if bool(self.plate) != bool(self.state):
            raise ValueError("Both license plate and state must be provided together.")


@dataclass(frozen=True)
class VehicleYear:
    value: int

    def __post_init__(self):
        import datetime
        current_year = datetime.date.today().year
        if not (current_year - 15 <= self.value <= current_year + 1):
            raise ValueError(
                f"Vehicle year {self.value} is outside the allowed range."
            )
