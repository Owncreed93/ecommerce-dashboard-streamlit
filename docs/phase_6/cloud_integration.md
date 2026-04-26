# Phase 6: Cloud Data Sourcing (OCI Integration)

## 1. Objective

Transition from local file storage to a cloud-native architecture using Oracle Cloud Infrastructure (OCI) Object Storage for dataset management, utilizing in-memory streaming to maintain a stateless application state and optimize compute resources.

## 2. Technical Requirements

### 2.1 Infrastructure

- OCI Object Storage: Hosting the production dataset (data.csv).
- Pre-Authenticated Request (PAR): A secure, time-limited URL for direct HTTPS access, managed as an environment variable (`OCI_PAR_URL`).

### 2.2 Application Logic

- Data Provider Utility: Implements a `DataProvider` interface.
- Hybrid Data Source Strategy: The application detects the presence of `OCI_PAR_URL`. If present, it streams from OCI; otherwise, it defaults to a local file path (development mode).
- Stream Processing: Uses Polars native URL-based data loading (`pl.scan_csv`) to stream data directly into memory.
- Stateless Architecture: Ensures zero write operations to the runtime environment.

### 2.3 Optimization Strategies

- Lazy Evaluation: Use `pl.scan_csv` with defined `dtypes` to minimize memory inference overhead.
- Streaming Mode: Enable `.collect(engine=True)` to process data in chunks.
- Query Pushdown: Enforce Predicate and Projection Pushdown by applying filters and selects before invoking the collection.

### 2.4 Performance Benchmarking (Efficiency Suite)

- Memory Footprint Tracking: Implement a utility to measure peak RSS during stream processing.
- Latency Profiling: Measure "Wall Time" for end-to-end execution.
- Engine Throughput: Calculate "Rows Per Second" processed.
- IO Optimization Audit: Verify the effectiveness of Pushdown techniques by comparing total rows scanned vs. rows read.

### 2.5 Security (OWASP 2025)

- Secrets Management: The OCI PAR URL must be retrieved via environment variables (e.g., `os.environ["OCI_PAR_URL"]`).
- No credentials or sensitive URLs shall be committed to the repository.

## 3. Validation and Stress Testing

- Cloud Data Flow: Verify that the application successfully establishes a streaming connection to the dataset on the first request.
- Stress Test: Simulate concurrent filter requests to monitor stability and performance degradation under load.
- Benchmark Report: Generate a performance audit log in the dashboard footer to display real-time efficiency metrics.
