"""Value objects for the identity bounded context.

Value objects are immutable and defined entirely by their attributes.
Two instances with the same attributes are equal. Each class enforces
its own invariants in __post_init__, making invalid states unrepresentable.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """A validated email address.

    Only a basic structural check is performed here. Full deliverability
    validation (DNS lookup, SMTP probe) is an infrastructure concern and
    does not belong in the domain.
    """

    address: str

    def __post_init__(self):
        if "@" not in self.address:
            raise ValueError(f"Invalid email address: {self.address}")


@dataclass(frozen=True)
class PersonName:
    """A person's name split into given names and surnames.

    Stored separately to support international naming conventions where
    family names may precede given names. String representation follows
    the "Surnames, Given names" convention used in the CustomUser model.
    """

    given_names: str
    surnames: str

    def __str__(self) -> str:
        return f"{self.surnames}, {self.given_names}"
