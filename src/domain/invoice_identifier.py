"""Value Object for invoice identification.

This module provides the InvoiceIdentifier class, ensuring validation
and business logic for invoice numbers.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InvoiceIdentifier:
    """A Value Object representing an invoice number.

    Enforces alphanumeric integrity and identifies cancellation transactions.

    Attributes:
        value: The raw invoice string.
    """

    value: str

    def __post_init__(self) -> None:
        """Validates the invoice format.

        Raises:
            ValueError: If the invoice contains non-alphanumeric characters.
        """
        if not self.value.isalnum():
            raise ValueError(f"Invalid characters in invoice: {self.value}")

    @property
    def is_cancellation(self) -> bool:
        """Checks if the invoice represents a cancellation.

        Returns:
            True if the invoice starts with 'C'.
        """
        return self.value.upper().startswith("C")
