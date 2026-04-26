"""Implementation of the KpiRepository using Polars.

This module provides the PolarsKpiRepository, which leverages the
Lazy API to process large datasets with minimal memory footprint.
"""

from datetime import datetime

import polars as pl

from domain.data_provider_interface import DataProvider
from domain.repository_interface import KpiRepository


class PolarsKpiRepository(KpiRepository):
    """Infrastructure implementation for KPI data access using Polars.

    Uses scan_csv and LazyFrame operations to optimize data retrieval
    from either local or remote data sources via a DataProvider.
    """

    def __init__(self, data_provider: DataProvider) -> None:
        """Initializes the repository with a DataProvider.

        Args:
            data_provider: The source provider to retrieve data location.
        """
        self.data_provider = data_provider

    def _get_lazy_frame(self) -> pl.LazyFrame:
        """Initializes a lazy scan of the data source with optimized types."""
        source = self.data_provider.ensure_data_is_available()

        # Define schema for memory efficiency
        schema = {
            "InvoiceNo": pl.String,
            "StockCode": pl.String,
            "Description": pl.String,
            "Quantity": pl.Int32,
            "UnitPrice": pl.Float64,
            "CustomerID": pl.Int32,
            "Country": pl.String,
        }

        return pl.scan_csv(
            source,
            encoding="utf8-lossy",
            schema_overrides=schema,
        )

    def get_lazy_data(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> pl.LazyFrame:
        """Retrieves and filters the dataset using Polars Lazy API.

        Args:
            country: Optional country filter.
            start_date: Optional start date filter.
            end_date: Optional end date filter.

        Returns:
            A filtered LazyFrame.
        """
        lf = self._get_lazy_frame()

        # Parse InvoiceDate
        lf = lf.with_columns(
            pl.col("InvoiceDate").str.to_datetime(format="%m/%d/%Y %H:%M")
        )

        # Apply Filters (Predicate Pushdown)
        if country:
            lf = lf.filter(pl.col("Country") == country)

        if start_date:
            lf = lf.filter(pl.col("InvoiceDate") >= start_date)

        if end_date:
            lf = lf.filter(pl.col("InvoiceDate") <= end_date)

        return lf

    def get_unique_countries(self) -> list[str]:
        """Retrieves a sorted list of unique countries in the dataset."""
        df = (
            self._get_lazy_frame()
            .select("Country")
            .unique()
            .sort("Country")
            .collect()
        )
        return df["Country"].to_list()

    def get_date_range(self) -> tuple[datetime, datetime]:
        """Retrieves the minimum and maximum dates in the dataset."""
        lf = self._get_lazy_frame().select(
            pl.col("InvoiceDate").str.to_datetime(format="%m/%d/%Y %H:%M")
        )
        stats = lf.select(
            [
                pl.col("InvoiceDate").min().alias("min_date"),
                pl.col("InvoiceDate").max().alias("max_date"),
            ]
        ).collect()

        return stats["min_date"][0], stats["max_date"][0]
