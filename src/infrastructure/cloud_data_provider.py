"""Cloud Data Provider infrastructure adapter.

This module implements the DataProvider interface for retrieving
dataset source URLs from environment variables for OCI Object Storage.
"""

import os
from typing import Final

from domain.data_provider_interface import DataProvider

OCI_PAR_URL_KEY: Final[str] = "OCI_PAR_URL"


class CloudDataProvider(DataProvider):
    """Infrastructure adapter for OCI-based data sourcing."""

    def ensure_data_is_available(self) -> str:
        """Retrieves the OCI PAR URL for streaming.

        Returns:
            The URL to the remote dataset.

        Raises:
            EnvironmentError: If the OCI_PAR_URL environment variable is not set.
        """
        url = os.environ.get(OCI_PAR_URL_KEY)
        if not url:
            raise OSError(
                f"Environment variable '{OCI_PAR_URL_KEY}' is not set."
            )
        return url
