"""Unit tests for the KpiTarget Value Object.

This module verifies that KpiTarget correctly evaluates performance
against defined business goals.
"""

import pytest

from domain.kpi_target import KpiTarget
from domain.kpi_value import KpiValue


def test_kpi_target_creation() -> None:
    """Verify that KpiTarget can be created with a goal value."""
    target = KpiTarget(goal=1000.0, unit="USD")
    assert target.goal == 1000.0
    assert target.unit == "USD"


def test_kpi_target_performance_evaluation() -> None:
    """Verify that KpiTarget correctly calculates percentage of goal reached."""
    target = KpiTarget(goal=100.0, unit="units")
    actual = KpiValue(value=85.0, unit="units")

    assert target.get_performance_percentage(actual) == 0.85


def test_kpi_target_different_units_raises_error() -> None:
    """Verify that comparing different units raises a ValueError."""
    target = KpiTarget(goal=100.0, unit="USD")
    actual = KpiValue(value=100.0, unit="EUR")

    with pytest.raises(ValueError, match="Unit mismatch"):
        target.get_performance_percentage(actual)


def test_kpi_target_is_immutable() -> None:
    """Verify that KpiTarget is immutable."""
    target = KpiTarget(goal=500.0, unit="pts")
    with pytest.raises(AttributeError):
        target.goal = 600.0  # type: ignore


def test_kpi_target_invalid_goal_raises_error() -> None:
    """Verify that a non-positive goal raises a ValueError."""
    with pytest.raises(ValueError, match="Goal must be greater than zero"):
        KpiTarget(goal=0.0, unit="USD")

    with pytest.raises(ValueError, match="Goal must be greater than zero"):
        KpiTarget(goal=-10.0, unit="USD")
