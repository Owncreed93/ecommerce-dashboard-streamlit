"""Value Object for customer identification.

This module provides the CustomerIdentifier class, ensuring consistency
and handling missing data for customer IDs.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CustomerIdentifier:
    """A Value Object representing a customer ID.

    Attributes:
        value: The raw customer identifier string or None.
    """

    value: str | None

    @property
    def is_missing(self) -> bool:
        """Checks if the customer ID is missing or empty.

        Returns:
            True if the identifier is not provided.
        """
        return self.value is None or str(self.value).strip() == ""

    def __repr__(self) -> str:
        """Returns the string representation of the identifier."""
        return self.value if not self.is_missing else "MISSING"
