# High-Performance Sales KPI Dashboard

A professional-grade dashboard designed to visualize Key Performance Indicators (KPIs) and Returns Analytics from large-scale retail datasets. This project is built following strict software engineering principles (DDD, TDD, SOLID) to ensure scalability and reliability.

## Project Overview

This application processes large datasets using Polars' high-efficiency engine to extract meaningful business metrics. It is designed to handle non-standard CSV encodings and complex data structures while maintaining a minimal memory footprint.

## Key Features

- Strategic KPIs: Total Revenue, Average Order Value (AOV), and Active Customer Base.
- Returns Analytics (Phase 4.5): Specialized tracking of return values and return rates with visual anomaly detection.
- Dynamic Filtering: Real-time filtering by Country and Date Range using Polars' Lazy API.
- Advanced Visualizations: Order value segmentation and peak hour analysis powered by Plotly.
- Data Integrity: Automatic handling of non-UTF8 characters and alphanumeric identifiers (e.g., cancellation codes starting with 'C').

## Architectural Principles

The project adheres to the following paradigms:

- Domain-Driven Design (DDD): Strict separation between Domain (Value Objects), Application (Services), and Infrastructure (Repositories).
- Value Objects: Immutable objects (Money, KpiValue, KpiDate) using frozen dataclasses with slots to ensure data integrity and memory efficiency.
- Clean Architecture: Core business logic is decoupled from the presentation layer (Streamlit) and data sources (CSV).
- TDD Workflow: Business logic is verified through a comprehensive suite of unit and integration tests.

## Technical Stack

- Language: Python 3.13.11+
- Data Engine: Polars (Lazy API) for memory-efficient large-scale processing.
- UI Framework: Streamlit.
- Testing: Pytest and Pytest-Cov (Current coverage: ~92%).
- Linter/Formatter: Ruff (Strict compliance with E, W, F, I, D, UP, B, ANN rules).
- Environment Management: Managed via uv.

## Performance Benchmarks

The system utilizes the Polars query engine to achieve industry-leading performance. Below are the metrics captured on a standard development machine:

| Metric | Production Baseline (541k rows) | Stress Test (1M synthetic rows) |
| :--- | :--- | :--- |
| **Total Latency** | **175.69 ms** | **462.19 ms** |
| **Memory Delta** | ~116 MB | ~394 MB |
| **Engine Throughput** | **3,084,470 rows/sec** | **2,163,592 rows/sec** |

### Key Technical Insights
- Instant UX: End-to-end processing time remains below the 500ms human perception threshold.
- Efficiency: The Lazy API architecture provides a 5x to 10x performance increase over traditional eager-loading implementations (e.g., standard Pandas).
- Scalability: Throughput is maintained above 2 million rows per second even with high-cardinality synthetic datasets.

## Getting Started

### Prerequisites
- Python 3.13
- uv (recommended)

### Commands (Makefile)
- make run: Execute the Streamlit dashboard locally.
- make test: Run the full test suite.
- make lint: Verify code quality using Ruff.
- make format: Apply automated code formatting.
- make cov: Generate a terminal coverage report.
- make requirements: Export project dependencies to requirements.txt.

## Project Roadmap
- Phase 1-3: Core Domain and Data Infrastructure (Completed).
- Phase 4: Streamlit Reactive Interface (Completed).
- Phase 4.5: Returns and Cancellations Analytics (Completed).
- Phase 5: Production Deployment and Audit (In Progress).
