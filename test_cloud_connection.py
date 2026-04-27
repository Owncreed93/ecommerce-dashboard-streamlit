"""Integration test for cloud data connection.

This module verifies that the HybridDataProvider can correctly resolve
the OCI PAR URL and that Polars can scan the remote CSV dataset.
"""

import os
import sys
from pathlib import Path

import polars as pl

# Setup path to find src
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from infrastructure.hybrid_data_provider import HybridDataProvider  # noqa: E402


def test_connection(force_fallback: bool = False) -> None:
    """Verifies the connection or fallback logic."""
    if force_fallback:
        if "OCI_PAR_URL" in os.environ:
            del os.environ["OCI_PAR_URL"]
        test_url = None
    else:
        test_url = os.environ.get(
            "OCI_PAR_URL",
            "https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv",
        )
        os.environ["OCI_PAR_URL"] = test_url

    print(f"Testing with URL: {test_url}")

    provider = HybridDataProvider(local_path="data/data.csv")
    resolved_path = provider.ensure_data_is_available()

    print(f"Resolved path from provider: {resolved_path}")

    try:
        # Try to scan the head of the file to verify connection
        lf = pl.scan_csv(resolved_path)
        df = lf.head(5).collect()
        print("Connection Successful! Preview:")
        print(df)
    except Exception as e:
        print(f"Connection Failed: {e}")


if __name__ == "__main__":
    test_connection(force_fallback=True)
