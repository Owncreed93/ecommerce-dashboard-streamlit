"""Repository interfaces for data access.

This module defines the abstract base classes that all repository
implementations must satisfy to ensure DDD decoupling.
"""

from abc import ABC, abstractmethod
from datetime import datetime

import polars as pl


class KpiRepository(ABC):
    """Abstract interface for KPI data access."""

    @abstractmethod
    def get_lazy_data(
        self,
        country: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> pl.LazyFrame:
        """Retrieves a filtered LazyFrame from the data source."""
        pass

    @abstractmethod
    def get_unique_countries(self) -> list[str]:
        """Retrieves a sorted list of unique countries in the dataset."""
        pass

    @abstractmethod
    def get_date_range(self) -> tuple[datetime, datetime]:
        """Retrieves the minimum and maximum dates in the dataset."""
        pass
