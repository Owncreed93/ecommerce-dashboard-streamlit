"""KpiValue Value Object for numerical metric representation.

This module provides the KpiValue class, which handles scaling and
formatting of business metrics.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class KpiValue:
    """A Value Object representing a numerical KPI result.

    Handles scaling for large numbers and specific unit formatting.

    Attributes:
        value: The numerical value of the KPI.
        unit: The unit of measurement (e.g., 'USD', '%', 'units').
    """

    value: Decimal
    unit: str

    def __post_init__(self) -> None:
        """Validates the KPI metadata.

        Raises:
            ValueError: If the unit is empty.
        """
        if not self.unit.strip():
            raise ValueError("Unit cannot be empty.")

    def format(self) -> str:
        """Formats the KPI value based on its magnitude and unit.

        Returns:
            A string representation of the formatted KPI.
        """
        if self.unit == "%":
            return f"{self.value * 100:.2f}%"

        abs_value = abs(self.value)
        if abs_value >= 1_000_000:
            scaled = self.value / Decimal("1000000")
            return f"{scaled:.1f}M {self.unit}"

        if abs_value >= 1_000:
            scaled = self.value / Decimal("1000")
            return f"{scaled:.1f}K {self.unit}"

        return f"{self.value:.2f} {self.unit}"
