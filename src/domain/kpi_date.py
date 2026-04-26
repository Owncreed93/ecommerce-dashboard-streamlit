"""KpiDate Value Object for temporal metric tracking.

This module provides the KpiDate class, ensuring ISO 8601 compliance
and date validation within the domain.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Self


@dataclass(frozen=True, slots=True)
class KpiDate:
    """A Value Object representing a date in the KPI domain.

    Ensures that all dates are handled as immutable objects and
    supports ISO 8601 formatting.

    Attributes:
        value: The datetime object.
    """

    value: datetime

    @classmethod
    def from_iso_string(cls, date_string: str) -> Self:
        """Creates a KpiDate from an ISO 8601 string.

        Args:
            date_string: The ISO formatted date string.

        Returns:
            A new KpiDate instance.

        Raises:
            ValueError: If the string is not a valid ISO 8601 date.
        """
        try:
            dt = datetime.fromisoformat(date_string)
            return cls(value=dt)
        except ValueError as e:
            raise ValueError(f"Invalid ISO 8601 date string: {date_string}") from e

    def to_iso_string(self) -> str:
        """Converts the date to an ISO 8601 string.

        Returns:
            The ISO formatted string.
        """
        return self.value.isoformat()
