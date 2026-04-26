"""Unit tests for the KpiDate Value Object.

This module verifies that KpiDate handles ISO 8601 formatting
and date validation correctly.
"""

from datetime import datetime

import pytest

from domain.kpi_date import KpiDate


def test_kpi_date_creation_from_string() -> None:
    """Verify that KpiDate can be created from an ISO string."""
    date_str = "2026-04-25T10:30:00"
    kpi_date = KpiDate.from_iso_string(date_str)
    assert kpi_date.value.year == 2026
    assert kpi_date.value.month == 4
    assert kpi_date.value.day == 25


def test_kpi_date_is_immutable() -> None:
    """Verify that KpiDate object is immutable."""
    kpi_date = KpiDate(value=datetime(2026, 4, 25))
    with pytest.raises(AttributeError):
        kpi_date.value = datetime(2026, 4, 26)  # type: ignore


def test_kpi_date_iso_format() -> None:
    """Verify that KpiDate returns correct ISO 8601 string."""
    dt = datetime(2026, 4, 25, 10, 30)
    kpi_date = KpiDate(value=dt)
    assert kpi_date.to_iso_string() == "2026-04-25T10:30:00"


def test_kpi_date_invalid_string_fails() -> None:
    """Verify that KpiDate raises ValueError for invalid date strings."""
    with pytest.raises(ValueError):
        KpiDate.from_iso_string("invalid-date")
