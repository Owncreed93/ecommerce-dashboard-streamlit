"""Hybrid Data Provider infrastructure adapter.

This module provides a provider that automatically switches between
cloud-based OCI streaming and local file-based data access,
supporting both environment variables and Streamlit secrets.
"""

import logging
import os
from typing import Final

import streamlit as st

from domain.data_provider_interface import DataProvider

OCI_PAR_URL_KEY: Final[str] = "OCI_PAR_URL"

# Initialize technical logger
logger = logging.getLogger(__name__)


class HybridDataProvider(DataProvider):
    """Infrastructure adapter that detects environment to provide data source."""

    def __init__(self, local_path: str) -> None:
        """Initializes the provider with a fallback local path.

        Args:
            local_path: The local path to the dataset for development.
        """
        self.local_path = local_path

    def ensure_data_is_available(self) -> str:
        """Detects environment and returns the appropriate data source URL/path.

        Supports OS environment variables and Streamlit secrets.

        Returns:
            The OCI PAR URL if in production (found in env or secrets),
            otherwise the local file path.
        """
        # 1. Try OS Environment Variable (PythonAnywhere/Local)
        url = os.environ.get(OCI_PAR_URL_KEY)

        # 2. Try Streamlit Secrets safely (Streamlit Cloud)
        if not url:
            try:
                if hasattr(st, "secrets") and OCI_PAR_URL_KEY in st.secrets:
                    url = st.secrets.get(OCI_PAR_URL_KEY)
            except Exception as e:
                logger.debug("Streamlit secrets not accessible: %s", str(e))

        if url:
            logger.info("Data source resolved to remote cloud URL.")
            return str(url)

        logger.warning(
            "OCI_PAR_URL not found. Falling back to local path: %s", self.local_path
        )
        return self.local_path
