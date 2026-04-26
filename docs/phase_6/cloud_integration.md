# Phase 6: Cloud Data Sourcing (OCI Integration)

## 1. Objective

Transition from local file storage to a Cloud-Native architecture using Oracle Cloud Infrastructure (OCI) Object Storage for dataset management and implement a performance audit suite to measure system efficiency.

## 2. Technical Requirements

### 2.1 Infrastructure

- OCI Object Storage: Hosting the production dataset (data.csv).
- Pre-Authenticated Request (PAR): A secure, time-limited URL for direct HTTPS access without requiring OCI SDK credentials in the application.

### 2.2 Application Logic

- Data Provider Utility: A new component to manage the data lifecycle.
- Download Manager: Checks for local presence of data.csv in the ephemeral storage of the Streamlit runtime.
- Stream Processing: Uses the `requests` or `httpx` library to download the dataset efficiently if missing.

### 2.3 Performance Benchmarking (Efficiency Suite)

- Memory Footprint Tracking: Implement a utility to measure peak RSS (Resident Set Size) during heavy Polars aggregations to verify constant memory usage.
- Latency Profiling: Measure "Wall Time" for end-to-end filter execution (from UI trigger to result materialization).
- Engine Throughput: Calculate "Rows Per Second" processed by the Polars Lazy API to demonstrate high-performance capabilities.
- IO Optimization Audit: Verify the effectiveness of Predicate and Projection Pushdown by comparing total rows scanned vs. rows read.

### 2.4 Security (OWASP 2025)

- Secrets Management: The OCI PAR URL must be stored in Streamlit Secrets (`st.secrets`).
- No credentials or sensitive URLs shall be committed to the GitHub repository.

## 3. Validation and Stress Testing

- Cloud Data Flow: Verify that the application successfully downloads the dataset during its first run on a fresh environment.
- Stress Test: Simulate concurrent filter requests to monitor stability and performance degradation.
- Benchmark Report: Generate a "Performance Audit" log in the dashboard footer to display real-time efficiency metrics (RAM, Latency, and Throughput).
