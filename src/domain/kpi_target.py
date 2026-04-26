"""KpiTarget Value Object for performance threshold logic.

This module provides the KpiTarget class, which manages business goals
and evaluates metrics against established targets.
"""

from dataclasses import dataclass

from domain.kpi_value import KpiValue


@dataclass(frozen=True, slots=True)
class KpiTarget:
    """A Value Object representing a business target or threshold.

    Attributes:
        goal: The numerical goal to reach.
        unit: The unit of measurement for the goal.
    """

    goal: float
    unit: str

    def __post_init__(self) -> None:
        """Validates the business goal.

        Raises:
            ValueError: If the goal is not greater than zero.
        """
        if self.goal <= 0:
            raise ValueError("Goal must be greater than zero.")

    def get_performance_percentage(self, actual: KpiValue) -> float:
        """Calculates the ratio between actual performance and the goal.

        Args:
            actual: The current KPI value to evaluate.

        Returns:
            A float representing the performance percentage (e.g., 0.85).

        Raises:
            ValueError: If the unit of the actual value does not match the goal.
            ZeroDivisionError: If the goal is zero.
        """
        if self.unit != actual.unit:
            raise ValueError(
                f"Unit mismatch: cannot compare goal in {self.unit} "
                f"with value in {actual.unit}"
            )

        if self.goal == 0:
            raise ZeroDivisionError("Cannot calculate performance against a zero goal.")

        return actual.value / self.goal
