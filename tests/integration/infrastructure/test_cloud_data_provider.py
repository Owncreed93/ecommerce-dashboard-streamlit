"""Tests for the CloudDataProvider infrastructure adapter."""

import os

import pytest

from infrastructure.cloud_data_provider import CloudDataProvider


def test_ensure_data_is_available_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifies that the URL is correctly retrieved from environment variables."""
    test_url = "https://example.com/data.csv"
    monkeypatch.setenv("OCI_PAR_URL", test_url)

    provider = CloudDataProvider()
    assert provider.ensure_data_is_available() == test_url

def test_ensure_data_is_available_missing_variable() -> None:
    """Verifies that an error is raised when the environment variable is missing."""
    # Ensure variable is not set
    if "OCI_PAR_URL" in os.environ:
        del os.environ["OCI_PAR_URL"]

    provider = CloudDataProvider()
    with pytest.raises(EnvironmentError, match="not set"):
        provider.ensure_data_is_available()
