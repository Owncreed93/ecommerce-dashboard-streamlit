"""Unit tests for the KPI Entity.

This module verifies that the KPI entity correctly encapsulates its
attributes and business logic.
"""

from datetime import datetime

from domain.kpi import KPI
from domain.kpi_date import KpiDate
from domain.kpi_target import KpiTarget
from domain.kpi_value import KpiValue


def test_kpi_creation() -> None:
    """Verify that a KPI can be created with its components."""
    value = KpiValue(value=1000.0, unit="USD")
    date = KpiDate(value=datetime(2026, 4, 25))
    target = KpiTarget(goal=1200.0, unit="USD")

    kpi = KPI(
        id="kpi-001",
        name="Total Sales",
        current_value=value,
        last_updated=date,
        target=target,
    )

    assert kpi.id == "kpi-001"
    assert kpi.name == "Total Sales"
    assert kpi.current_value == value


def test_kpi_performance_summary() -> None:
    """Verify that KPI provides a valid performance percentage."""
    kpi = KPI(
        id="1",
        name="Test",
        current_value=KpiValue(50, "units"),
        last_updated=KpiDate(datetime.now()),
        target=KpiTarget(100, "units"),
    )

    assert kpi.performance_ratio == 0.5


def test_kpi_without_target_ratio_is_none() -> None:
    """Verify that performance_ratio is None if no target is set."""
    kpi = KPI(
        id="1",
        name="Test",
        current_value=KpiValue(50, "units"),
        last_updated=KpiDate(datetime.now()),
        target=None,
    )

    assert kpi.performance_ratio is None
