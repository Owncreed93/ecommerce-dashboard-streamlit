# Architectural Design Document: KPI Dashboard

## 1. System Scaffolding

The project follows a flattened modular structure under the src/ directory to facilitate direct imports and maintain a clear separation of concerns according to Domain-Driven Design (DDD).

```text
/
├── data/               # Raw CSV datasets
├── docs/               # Implementation phases and roadmaps
├── src/                # Root source directory
│   ├── application/    # Use cases and orchestration (Services)
│   ├── domain/         # Core business logic (Entities, Value Objects)
│   └── infrastructure/ # External tools (Polars, Repositories)
├── tests/              # TDD suite (Unit, Integration)
├── main.py             # Streamlit entry point
└── pyproject.toml      # Dependency and tool configuration
```

## 2. Architectural Patterns

### 2.1 Domain-Driven Design (DDD)
- Domain Layer: Contains immutable Value Objects (Money, KpiValue, KpiDate) and Entities. It has zero external dependencies.
- Application Layer: Orchestrates data flow between the Domain and Infrastructure layers. It transforms raw data into domain-specific objects.
- Infrastructure Layer: Implements technical details, specifically the PolarsKpiRepository, which translates CSV data into business metrics.

### 2.2 Repository Pattern
Data access is decoupled from business logic through an abstract interface. This allows for switching data sources (e.g., from CSV to a SQL database) without impacting the application or domain layers.

### 2.3 Value Objects and Immutability
Domain attributes are modeled as dataclasses with `frozen=True` and `slots=True`.
- Memory Optimization: slots reduces RAM consumption by preventing the creation of `__dict__`.
- Data Integrity: frozen ensures objects remain immutable after instantiation.

## 3. Data Processing Strategy (Polars Lazy API)

To handle large-scale datasets efficiently, the system utilizes the Polars Lazy API:
- Predicate Pushdown: Filters are applied at the scan level to minimize data loading.
- Projection Pushdown: Only required columns are read from the disk.
- Memory Efficiency: Calculations are performed in the Polars engine (C++), materializing only final results.

### 3.1 Data Integrity and Robustness
- Encoding: Uses `utf8-lossy` encoding in `scan_csv` to handle non-standard characters in retail datasets without raising exceptions.
- Schema Overrides: Explicitly treats `InvoiceNo` and `CustomerID` as String types to prevent parsing errors when alphanumeric cancellation codes (e.g., starting with 'C') are encountered.

## 4. Design Principles

- SOLID: Application depends on Abstractions, not Implementations (Dependency Inversion).
- KISS/DRY: Business logic is centralized in the Domain and Application layers.
- TDD: Every feature is backed by automated tests before implementation.

## 5. UI/UX and State Management

The Streamlit interface acts as a reactive consumer of the Application layer.
- Reactive Filtering: Sidebar inputs act as state flags that drive the Polars query engine.
- Visual Feedback: Utilizes color-coded anomaly detection for the Returns Analytics module (Phase 4.5), applying the Von Restorff effect for critical metrics.
