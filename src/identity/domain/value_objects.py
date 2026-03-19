from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    address: str

    def __post_init__(self):
        if "@" not in self.address:
            raise ValueError(f"Invalid email address: {self.address}")


@dataclass(frozen=True)
class PersonName:
    given_names: str
    surnames: str

    def __str__(self) -> str:
        return f"{self.surnames}, {self.given_names}"
