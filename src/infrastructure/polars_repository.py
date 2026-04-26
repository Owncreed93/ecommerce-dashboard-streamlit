"""Implementation of the KpiRepository using Polars.

This module provides the PolarsKpiRepository, which leverages the
Lazy API to process large CSV datasets with minimal memory footprint.
"""

from datetime import datetime

import polars as pl

from domain.repository_interface import KpiRepository


class PolarsKpiRepository(KpiRepository):
    """Infrastructure implementation for KPI data access using Polars.

    Uses scan_csv and LazyFrame operations to optimize data retrieval.
    """

    def __init__(self, file_path: str) -> None:
        """Initializes the repository with the path to the CSV file.

        Args:
            file_path: Absolute or relative path to data.csv.
        """
        self.file_path = file_path

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
        # Scan the CSV lazily with utf8-lossy encoding and explicit string types
        lf = pl.scan_csv(
            self.file_path,
            encoding="utf8-lossy",
            schema_overrides={"InvoiceNo": pl.String, "CustomerID": pl.String}
        )

        # Parse InvoiceDate (e.g., 12/1/2010 8:26)
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
            pl.scan_csv(
                self.file_path,
                encoding="utf8-lossy",
                schema_overrides={"InvoiceNo": pl.String}
            )
            .select("Country")
            .unique()
            .sort("Country")
            .collect()
        )
        return df["Country"].to_list()

    def get_date_range(self) -> tuple[datetime, datetime]:
        """Retrieves the minimum and maximum dates in the dataset."""
        lf = pl.scan_csv(
            self.file_path,
            encoding="utf8-lossy",
            schema_overrides={"InvoiceNo": pl.String}
        ).select(
            pl.col("InvoiceDate").str.to_datetime(format="%m/%d/%Y %H:%M")
        )
        stats = lf.select(
            [
                pl.col("InvoiceDate").min().alias("min_date"),
                pl.col("InvoiceDate").max().alias("max_date"),
            ]
        ).collect()

        return stats["min_date"][0], stats["max_date"][0]
