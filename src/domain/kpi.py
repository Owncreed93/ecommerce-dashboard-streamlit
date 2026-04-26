"""KPI Entity representing a business metric.

This module provides the KPI class, which serves as the aggregate root
for business indicators.
"""

from dataclasses import dataclass

from domain.kpi_date import KpiDate
from domain.kpi_target import KpiTarget
from domain.kpi_value import KpiValue


@dataclass(slots=True)
class KPI:
    """An Entity representing a specific Key Performance Indicator.

    Attributes:
        id: Unique identifier for the KPI.
        name: Human-readable name of the metric.
        current_value: The latest calculated result.
        last_updated: The date of the last calculation.
        target: Optional business goal for this KPI.
    """

    id: str
    name: str
    current_value: KpiValue
    last_updated: KpiDate
    target: KpiTarget | None = None

    @property
    def performance_ratio(self) -> float | None:
        """Calculates the ratio of current value vs target goal.

        Returns:
            A float between 0 and 1 (or more), or None if no target exists.
        """
        if self.target is None:
            return None
        return self.target.get_performance_percentage(self.current_value)
