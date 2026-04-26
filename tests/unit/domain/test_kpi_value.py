"""Unit tests for the KpiValue Value Object.

This module verifies that KpiValue handles numerical validation,
formatting, and immutability correctly.
"""

import pytest

from domain.kpi_value import KpiValue


def test_kpi_value_creation() -> None:
    """Verify that KpiValue can be created with a float value."""
    kpi = KpiValue(value=1500.50, unit="USD")
    assert kpi.value == 1500.50
    assert kpi.unit == "USD"


def test_kpi_value_is_immutable() -> None:
    """Verify that KpiValue object is immutable."""
    kpi = KpiValue(value=100.0, unit="%")
    with pytest.raises(AttributeError):
        kpi.value = 200.0  # type: ignore


def test_kpi_value_formatting_large_numbers() -> None:
    """Verify that KpiValue scales large numbers for display."""
    kpi = KpiValue(value=1_200_000.0, unit="USD")
    assert kpi.format() == "1.2M USD"


def test_kpi_value_formatting_percentage() -> None:
    """Verify that KpiValue formats percentages correctly."""
    kpi = KpiValue(value=0.856, unit="%")
    assert kpi.format() == "85.60%"


def test_kpi_value_negative_validation() -> None:
    """Verify that KpiValue can handle negative values if allowed."""
    kpi = KpiValue(value=-10.5, unit="pts")
    assert kpi.value == -10.5


def test_kpi_value_invalid_unit_raises_error() -> None:
    """Verify that an empty unit raises a ValueError."""
    with pytest.raises(ValueError, match="Unit cannot be empty"):
        KpiValue(value=100.0, unit="")
