"""Application service for KPI orchestration.

This module provides the KpiService, which calculates business metrics
using the Repository abstraction and returning Domain Objects.
"""

from datetime import datetime
from decimal import Decimal

import polars as pl

from domain.kpi_value import KpiValue
from domain.money import Money
from domain.repository_interface import KpiRepository
from domain.transaction_type import TransactionType


class KpiService:
    """Orchestrator for business metric calculations.

    This service ensures that logic is independent of the data source
    by using the KpiRepository interface.
    """

    def __init__(self, repository: KpiRepository) -> None:
        """Initializes the service with a repository.

        Args:
            repository: An implementation of the KpiRepository interface.
        """
        self.repository = repository

    def _apply_transaction_filter(
        self, lf: pl.LazyFrame, trans_type: TransactionType
    ) -> pl.LazyFrame:
        """Internal helper to filter transactions by type.

        Uses the 'C' prefix pattern defined in InvoiceIdentifier.

        Args:
            lf: The input LazyFrame.
            trans_type: The transaction category to filter by.

        Returns:
            A filtered LazyFrame.
        """
        if trans_type == TransactionType.SALES:
            # Sales are transactions with positive quantity and no 'C' prefix
            return lf.filter(
                (pl.col("Quantity") > 0) & (~pl.col("InvoiceNo").str.starts_with("C"))
            )
        if trans_type == TransactionType.RETURNS:
            # Returns/Cancellations start with 'C'
            return lf.filter(pl.col("InvoiceNo").str.starts_with("C"))
        return lf

    def get_filters_data(self) -> dict:
        """Retrieves dynamic data for UI filters.

        Returns:
            A dictionary containing countries and date ranges.
        """
        return {
            "countries": self.repository.get_unique_countries(),
            "date_range": self.repository.get_date_range(),
        }

    def get_total_revenue(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        trans_type: TransactionType = TransactionType.ALL,
    ) -> Money:
        """Calculates the total revenue for a given filter.

        Args:
            country: Optional country filter.
            start_date: Optional start date.
            end_date: Optional end date.
            trans_type: Type of transactions to include.

        Returns:
            A Money object containing the total revenue.
        """
        lf = self.repository.get_lazy_data(
            country=country, start_date=start_date, end_date=end_date
        )
        lf = self._apply_transaction_filter(lf, trans_type)

        # Calculate sum of Quantity * UnitPrice
        result = lf.select(
            (pl.col("Quantity") * pl.col("UnitPrice")).sum().alias("total")
        ).collect()

        total_val = result["total"][0] if result.height > 0 else 0.0
        # For returns only, we show the absolute value in revenue cards
        if trans_type == TransactionType.RETURNS:
            total_val = abs(total_val)

        return Money(amount=Decimal(str(round(total_val, 2))), currency="USD")

    def get_average_order_value(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        trans_type: TransactionType = TransactionType.ALL,
    ) -> KpiValue:
        """Calculates the average order value (AOV).

        AOV = Total Revenue / Unique Order Count.

        Args:
            country: Optional country filter.
            start_date: Optional start date.
            end_date: Optional end date.
            trans_type: Type of transactions to include.

        Returns:
            A KpiValue object representing the AOV.
        """
        lf = self.repository.get_lazy_data(
            country=country, start_date=start_date, end_date=end_date
        )
        lf = self._apply_transaction_filter(lf, trans_type)

        # Calculate Revenue and Unique Invoice count in a single pass
        stats = lf.select(
            [
                (pl.col("Quantity") * pl.col("UnitPrice")).sum().alias("revenue"),
                pl.col("InvoiceNo").n_unique().alias("order_count"),
            ]
        ).collect()

        if stats.height == 0 or stats["order_count"][0] == 0:
            return KpiValue(value=Decimal("0.0"), unit="USD")

        rev = stats["revenue"][0]
        if trans_type == TransactionType.RETURNS:
            rev = abs(rev)

        aov = rev / stats["order_count"][0]
        return KpiValue(value=Decimal(str(round(aov, 2))), unit="USD")

    def get_active_customers_count(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        trans_type: TransactionType = TransactionType.ALL,
    ) -> int:
        """Calculates the number of unique customers.

        Args:
            country: Optional country filter.
            start_date: Optional start date.
            end_date: Optional end date.
            trans_type: Type of transactions to include.

        Returns:
            An integer representing the count of unique CustomerIDs.
        """
        lf = self.repository.get_lazy_data(
            country=country, start_date=start_date, end_date=end_date
        )
        lf = self._apply_transaction_filter(lf, trans_type)

        result = lf.select(
            pl.col("CustomerID").n_unique().alias("customer_count")
        ).collect()

        return result["customer_count"][0] if result.height > 0 else 0

    def get_order_segmentation(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        trans_type: TransactionType = TransactionType.ALL,
    ) -> dict[str, int]:
        """Segments orders into Low, Mid, and High value categories.

        Args:
            country: Optional country filter.
            start_date: Optional start date.
            end_date: Optional end date.
            trans_type: Type of transactions to include.

        Returns:
            A dictionary with the count of orders in each segment.
        """
        lf = self.repository.get_lazy_data(
            country=country, start_date=start_date, end_date=end_date
        )
        lf = self._apply_transaction_filter(lf, trans_type)

        # Group by InvoiceNo to get total per order
        order_totals = lf.group_by("InvoiceNo").agg(
            (pl.col("Quantity") * pl.col("UnitPrice")).abs().sum().alias("order_total")
        )

        # Define segments
        segmented = order_totals.with_columns(
            pl.when(pl.col("order_total") < 50)
            .then(pl.lit("Low"))
            .when(pl.col("order_total") < 200)
            .then(pl.lit("Mid"))
            .otherwise(pl.lit("High"))
            .alias("segment")
        )

        # Aggregate segments
        result = segmented.group_by("segment").len().collect()

        return dict(zip(result["segment"], result["len"], strict=False))

    def get_peak_hours(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        trans_type: TransactionType = TransactionType.ALL,
    ) -> dict[int, int]:
        """Calculates order counts per hour of the day.

        Args:
            country: Optional country filter.
            start_date: Optional start date.
            end_date: Optional end date.
            trans_type: Type of transactions to include.

        Returns:
            A dictionary with hour as key and order count as value.
        """
        lf = self.repository.get_lazy_data(
            country=country, start_date=start_date, end_date=end_date
        )
        lf = self._apply_transaction_filter(lf, trans_type)

        # Ensure each InvoiceNo is counted only once (Integrity Fix)
        # We sort by date to consistently pick the earliest occurrence per invoice
        result = (
            lf.sort("InvoiceDate")
            .unique("InvoiceNo", keep="first")
            .with_columns(pl.col("InvoiceDate").dt.hour().alias("hour"))
            .group_by("hour")
            .agg(pl.len().alias("count"))
            .sort("hour")
            .collect()
        )

        return dict(zip(result["hour"], result["count"], strict=False))

    def get_returns_metrics(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict:
        """Calculates returns value and return rate.

        Args:
            country: Optional country filter.
            start_date: Optional start date.
            end_date: Optional end date.

        Returns:
            A dictionary containing:
            - total_returns: Money object (sum of absolute returns).
            - return_rate: KpiValue object (Returns / Gross Sales).
        """
        lf = self.repository.get_lazy_data(
            country=country, start_date=start_date, end_date=end_date
        )

        # Calculate Gross Sales and Returns in parallel
        # Gross sales exclude 'C' prefix and have positive quantity
        # Returns include 'C' prefix
        stats = lf.select(
            [
                pl.when(
                    (pl.col("Quantity") > 0)
                    & (~pl.col("InvoiceNo").str.starts_with("C"))
                )
                .then(pl.col("Quantity") * pl.col("UnitPrice"))
                .otherwise(0.0)
                .sum()
                .alias("gross_sales"),
                pl.when(pl.col("InvoiceNo").str.starts_with("C"))
                .then((pl.col("Quantity") * pl.col("UnitPrice")).abs())
                .otherwise(0.0)
                .sum()
                .alias("returns_value"),
            ]
        ).collect()

        gross = stats["gross_sales"][0] if stats.height > 0 else 0.0
        returns = stats["returns_value"][0] if stats.height > 0 else 0.0

        return_rate = (returns / gross) if gross > 0 else 0.0

        return {
            "total_returns": Money(
                amount=Decimal(str(round(returns, 2))), currency="USD"
            ),
            "return_rate": KpiValue(value=round(return_rate, 4), unit="%"),
        }
