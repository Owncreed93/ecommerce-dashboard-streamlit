"""Data Provider interface for infrastructure adapters.

This module defines the contract for data retrieval components,
ensuring the application layer remains agnostic of the data source.
"""

from abc import ABC, abstractmethod


class DataProvider(ABC):
    """Interface for data sourcing components."""

    @abstractmethod
    def ensure_data_is_available(self) -> str:
        """Ensures the dataset is locally available.

        Returns:
            The path to the local dataset.
        """
