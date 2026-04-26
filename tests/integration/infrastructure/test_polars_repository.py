"""Integration tests for the PolarsKpiRepository.

This module verifies that the repository correctly filters, cleans,
and processes data using the Polars Lazy API.
"""

from datetime import datetime
from pathlib import Path

import polars as pl
import pytest

from infrastructure.polars_repository import PolarsKpiRepository


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Creates a sample CSV file for integration testing."""
    csv_path = tmp_path / "test_data.csv"
    data = {
        "InvoiceNo": ["536365", "536365", "536367", "536368"],
        "StockCode": ["85123A", "71053", "84879", "22752"],
        "Description": ["Item A", "Item B", "Item C", "Item D"],
        "Quantity": [6, 1, 32, 2],
        "InvoiceDate": [
            "12/1/2010 8:26",
            "12/1/2010 8:26",
            "12/1/2010 8:34",
            "12/2/2010 10:00",
        ],
        "UnitPrice": [2.55, 3.39, 1.69, 7.65],
        "CustomerID": ["17850", "17850", "13047", None],
        "Country": ["United Kingdom", "United Kingdom", "United Kingdom", "France"],
    }
    df = pl.DataFrame(data)
    df.write_csv(csv_path)
    return csv_path


def test_repository_loads_and_filters_by_country(sample_csv: Path) -> None:
    """Verify that the repository filters data by country correctly."""
    repo = PolarsKpiRepository(file_path=str(sample_csv))
    lazy_df = repo.get_lazy_data(country="France")

    result = lazy_df.collect()
    assert result.height == 1
    assert result["Country"][0] == "France"


def test_repository_filters_by_date_range(sample_csv: Path) -> None:
    """Verify that the repository filters data by date range correctly."""
    repo = PolarsKpiRepository(file_path=str(sample_csv))
    start = datetime(2010, 12, 1, 0, 0)
    end = datetime(2010, 12, 1, 23, 59)

    lazy_df = repo.get_lazy_data(start_date=start, end_date=end)
    result = lazy_df.collect()

    assert result.height == 3


def test_repository_handles_null_customer_id(sample_csv: Path) -> None:
    """Verify that null CustomerIDs are handled (e.g., filled or cast)."""
    repo = PolarsKpiRepository(file_path=str(sample_csv))
    lazy_df = repo.get_lazy_data()
    result = lazy_df.collect()

    # Check that CustomerID is correctly cast (should be Float64 or Int64
    # depending on implementation)
    assert result["CustomerID"].null_count() == 1


def test_repository_gets_unique_countries(sample_csv: Path) -> None:
    """Verify that the repository retrieves all unique countries."""
    repo = PolarsKpiRepository(file_path=str(sample_csv))
    countries = repo.get_unique_countries()

    assert "United Kingdom" in countries
    assert "France" in countries
    assert len(countries) == 2


def test_repository_gets_date_range(sample_csv: Path) -> None:
    """Verify that the repository retrieves correct min and max dates."""
    repo = PolarsKpiRepository(file_path=str(sample_csv))
    min_date, max_date = repo.get_date_range()

    assert isinstance(min_date, datetime)
    assert isinstance(max_date, datetime)
    assert min_date.day == 1
    assert max_date.day == 2
