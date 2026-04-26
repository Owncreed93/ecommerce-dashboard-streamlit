"""Money Value Object and related financial logic.

This module provides the Money class, ensuring high-precision financial
calculations using Decimals and protecting business invariants.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Self


@dataclass(frozen=True, slots=True)
class Money:
    """A Value Object representing a monetary amount with high precision.

    This class ensures financial calculations are performed using Decimals
    to avoid floating-point inaccuracies. It is immutable and optimized
    for memory usage via slots.

    Attributes:
        amount: The monetary value as a Decimal.
        currency: The ISO currency code (e.g., 'USD').
    """

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        """Validates the financial metadata.

        Raises:
            ValueError: If the currency is empty.
        """
        if not self.currency.strip():
            raise ValueError("Currency cannot be empty.")

    @classmethod
    def from_float(cls, amount: float, currency: str) -> Self:
        """Creates a Money instance from a float amount.

        Args:
            amount: The monetary value as a float.
            currency: The ISO currency code.

        Returns:
            A new Money instance.
        """
        return cls(amount=Decimal(str(amount)), currency=currency)

    def __add__(self, other: Self) -> Self:
        """Adds two Money objects of the same currency.

        Args:
            other: The other Money object to add.

        Returns:
            A new Money instance with the sum.

        Raises:
            ValueError: If the currencies do not match.
        """
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add different currencies: {self.currency} and {other.currency}"
            )

        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __repr__(self) -> str:
        """Returns a string representation of the Money object."""
        return f"{self.amount} {self.currency}"
