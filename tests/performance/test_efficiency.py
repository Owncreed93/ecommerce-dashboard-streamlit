"""Performance benchmarking for the KPI Dashboard.

This module measures memory footprint and latency to verify the efficiency
of the Polars Lazy API and the project architecture.
"""

import os
import time

import psutil
import pytest

from application.kpi_service import KpiService
from infrastructure.local_file_data_provider import LocalFileDataProvider
from infrastructure.polars_repository import PolarsKpiRepository


def get_memory_usage_mb() -> float:
    """Returns the current process memory usage in MB.

    Returns:
        Memory usage in Megabytes.
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


@pytest.fixture
def service() -> KpiService:
    """Provides a production-ready KpiService instance.

    Uses stress_test.csv if the STRESS_TEST environment variable is set.
    """
    is_stress = os.getenv("STRESS_TEST") == "1"
    file_path = "data/stress_test.csv" if is_stress else "data/data.csv"

    provider = LocalFileDataProvider(file_path=file_path)
    repo = PolarsKpiRepository(data_provider=provider)
    return KpiService(repository=repo)


def test_efficiency_baseline(service: KpiService) -> None:
    """Measures latency and memory footprint for a full dataset scan.

    This benchmark quantifies:
    1. Execution time (Latency).
    2. Peak memory consumption.
    3. Engine throughput (Rows/sec).
    """
    is_stress = os.getenv("STRESS_TEST") == "1"
    total_rows = 1_000_000 if is_stress else 541909
    label = "STRESS TEST (SYNTHETIC)" if is_stress else "PRODUCTION BASELINE"

    # 1. Capture initial state
    start_memory = get_memory_usage_mb()
    start_time = time.perf_counter()

    # 2. Trigger heavy calculations
    # Note: These operations use the Polars Lazy API
    revenue = service.get_total_revenue()
    _ = service.get_average_order_value()
    _ = service.get_active_customers_count()
    _ = service.get_order_segmentation()

    # 3. Capture end state
    end_time = time.perf_counter()
    end_memory = get_memory_usage_mb()

    # 4. Metrics calculation
    latency_ms = (end_time - start_time) * 1000
    memory_delta_mb = end_memory - start_memory
    throughput = total_rows / (end_time - start_time)

    # 5. Reporting
    print(f"\n--- {label} AUDIT REPORT ---")
    print(f"Dataset Size: {total_rows:,} rows")
    print(f"Total Latency: {latency_ms:.2f} ms")
    print(f"Memory Delta: {memory_delta_mb:.2f} MB")
    print(f"Engine Throughput: {throughput:,.0f} rows/sec")
    print("--------------------------------\n")

    # 6. Assertions for technical efficiency
    # Baseline for 500k rows: 150MB | Stress test for 1M high-cardinality rows: 500MB
    # Latency goal is always sub-second (1000ms)
    mem_limit = 500 if is_stress else 150

    assert latency_ms < 1000, f"Latency too high: {latency_ms}ms"
    assert memory_delta_mb < mem_limit, (
        f"Memory footprint too high: {memory_delta_mb}MB"
    )
    assert revenue.amount != 0
