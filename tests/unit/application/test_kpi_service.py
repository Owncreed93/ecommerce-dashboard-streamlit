"""Unit tests for the KpiService application layer.

This module verifies that the KpiService correctly orchestrates
KPI calculations using mocked repository data.
"""

from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import polars as pl
import pytest

from application.kpi_service import KpiService
from domain.money import Money
from domain.repository_interface import KpiRepository
from domain.segmentation_thresholds import SegmentationThresholds


@pytest.fixture
def mock_repo() -> MagicMock:
    """Provides a mocked KpiRepository."""
    repo = MagicMock(spec=KpiRepository)

    # Sample data for testing
    data = {
        "InvoiceNo": ["1", "1", "2"],
        "Quantity": [2, 3, 10],
        "UnitPrice": [10.0, 10.0, 5.0],
        "CustomerID": ["C1", "C1", "C2"],
        "Country": ["UK", "UK", "UK"],
    }
    # (2*10) + (3*10) + (10*5) = 20 + 30 + 50 = 100
    repo.get_lazy_data.return_value = pl.LazyFrame(data)

    # Default thresholds for testing
    repo.get_revenue_quantiles.return_value = SegmentationThresholds(
        low_bound=Decimal("40.0"), high_bound=Decimal("150.0")
    )

    return repo


def test_get_total_revenue(mock_repo: MagicMock) -> None:
    """Verify that total revenue is calculated with Decimal precision."""
    service = KpiService(repository=mock_repo)
    revenue = service.get_total_revenue()

    assert isinstance(revenue, Money)
    assert revenue.amount == Decimal("100.00")
    assert revenue.currency == "USD"


def test_get_average_order_value(mock_repo: MagicMock) -> None:
    """Verify that AOV is calculated correctly (Total / Unique Orders)."""
    # Total Revenue = 100, Unique Orders = 2 (InvoiceNo 1 and 2)
    # AOV = 100 / 2 = 50
    service = KpiService(repository=mock_repo)
    aov = service.get_average_order_value()

    assert aov.value == 50.0
    assert aov.unit == "USD"


def test_get_active_customers(mock_repo: MagicMock) -> None:
    """Verify that active customers count is correct."""
    service = KpiService(repository=mock_repo)
    count = service.get_active_customers_count()

    assert count == 2


def test_get_order_segmentation(mock_repo: MagicMock) -> None:
    """Verify that orders are correctly segmented using dynamic thresholds."""
    # Order 1: (2*10) + (3*10) = 50. Low=40, High=150. 50 is "Mid".
    # Order 2: 10*5 = 50. 50 is "Mid".
    # Expected: 2 Mid.
    service = KpiService(repository=mock_repo)
    segmentation = service.get_order_segmentation()

    assert segmentation["counts"]["Mid"] == 2
    assert segmentation["thresholds"]["low"] == Decimal("40.0")
    assert segmentation["thresholds"]["high"] == Decimal("150.0")


def test_get_peak_hours(mock_repo: MagicMock) -> None:
    """Verify that peak shopping hours are correctly aggregated."""
    # Adding timestamp to mock data for this specific test
    data = {
        "InvoiceNo": ["1", "2"],
        "InvoiceDate": [
            datetime(2026, 4, 25, 10, 0),  # Hour 10
            datetime(2026, 4, 25, 10, 30),  # Hour 10
        ],
        "Quantity": [1, 1],
        "UnitPrice": [10.0, 10.0],
    }
    mock_repo.get_lazy_data.return_value = pl.LazyFrame(data)

    service = KpiService(repository=mock_repo)
    peaks = service.get_peak_hours()

    assert peaks[10] == 2


def test_get_peak_hours_integrity(mock_repo: MagicMock) -> None:
    """Verify that a single InvoiceNo is counted only once in the histogram.

    Scenario: Invoice 'C1' has two lines with slightly different timestamps
    that fall into different hours (e.g., 10:59 and 11:00). It should only
    be counted once.
    """
    data = {
        "InvoiceNo": ["C1", "C1"],
        "InvoiceDate": [
            datetime(2026, 4, 25, 10, 59),
            datetime(2026, 4, 25, 11, 00),
        ],
        "Quantity": [-1, -1],
        "UnitPrice": [10.0, 10.0],
    }
    mock_repo.get_lazy_data.return_value = pl.LazyFrame(data)

    service = KpiService(repository=mock_repo)
    peaks = service.get_peak_hours()

    # It should be counted only once (at hour 10)
    assert peaks.get(10, 0) == 1
    assert peaks.get(11, 0) == 0


def test_get_filters_data(mock_repo: MagicMock) -> None:
    """Verify that filter data is retrieved correctly from repository."""
    mock_repo.get_unique_countries.return_value = ["UK", "France"]
    mock_repo.get_date_range.return_value = (datetime(2010, 1, 1), datetime(2011, 1, 1))

    service = KpiService(repository=mock_repo)
    filters = service.get_filters_data()

    assert "UK" in filters["countries"]
    assert filters["date_range"][0].year == 2010


def test_get_returns_metrics(mock_repo: MagicMock) -> None:
    """Verify calculation of returns and return rate.

    Data:
    - Gross Sales: (10 * 10) = 100
    - Returns: abs(-2 * 10) = 20
    - Total Net: 80
    - Return Rate: 20 / 100 = 20% (0.20)
    """
    data = {
        "InvoiceNo": ["1", "C1"],
        "Quantity": [10, -2],
        "UnitPrice": [10.0, 10.0],
        "Country": ["UK", "UK"],
    }
    mock_repo.get_lazy_data.return_value = pl.LazyFrame(data)

    service = KpiService(repository=mock_repo)
    metrics = service.get_returns_metrics()

    assert metrics["total_returns"].amount == Decimal("20.00")
    assert metrics["return_rate"].value == 0.20
    assert metrics["return_rate"].unit == "%"
