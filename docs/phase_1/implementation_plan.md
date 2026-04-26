# Implementation Plan: High-Performance KPI Dashboard Portfolio

## 1. Project Objective

Develop a professional-grade KPI Dashboard for Streamlit Cloud deployment. This project implements Domain-Driven Design (DDD) to visualize business metrics from the `data/data.csv` dataset, using Polars for high-efficiency data processing.

## 2. Defined Business KPIs & Statistical Metrics

The system will support dynamic filtering (by Country, Date, and Order Value) and provide the following insights:

### 2.1 Strategic KPIs

1. **Total Revenue:** Sum of (`Quantity` * `UnitPrice`) with `Decimal` precision.
2. **Average Order Value (AOV):** Dynamic calculation using `pl.Int64` for counting and `pl.Float64` for division.
3. **Active Customer Base:** Distinct count of `CustomerID`.

### 2.2 Statistical & Distribution Metrics

4. **Order Value Segmentation:** Distribution analysis grouping orders into categories (e.g., Low, Mid, High value) to identify customer segments.
2. **Peak Shopping Hours by Country:** Temporal patterns to identify peak traffic windows.
3. **Revenue Contribution %:** Percentage of total income generated per Country or Product Line.
4. **Sales Velocity:** Total units sold over time periods.

## 3. Technical Stack

- **Language:** Python 3.13.
- **Data Engine:** Polars (Lazy API for efficient dynamic filtering).
- **Frontend:** Streamlit (Sidebar filters acting as state flags).
- **Logic:** Application Services (Orchestration) and Domain Entities (Business rules).
- **Testing:** Pytest.
- **Linter/Formatter:** Ruff.

## 4. Implementation Phases

### Phase 1: Domain Layer and Value Objects (Current)

- **Scope:** Define immutable Value Objects using `frozen=True` dataclasses with `slots=True`.
- **Key Objects:**
  - `Money`: High-precision financial calculations.
  - `KpiValue`: Wrapper for metrics and statistical figures.
  - `KpiDate`: Temporal validation.
- **Validation:** Unit tests for precision and immutability.

### Phase 2: Data Infrastructure (Repository Pattern)

- **Scope:** Polars-based repository. Implements dynamic filtering logic within `scan_csv` to act as a "Virtual Database".
- **Validation:** Integration tests for filtered data retrieval.

### Phase 3: Application Services (Business Logic)

- **Scope:** Orchestrate calculations (Percentages, Segmentations, Aggregations).
- **Validation:** Unit tests verifying that logic is independent of the data source.

### Phase 4: Streamlit Interface

- **Scope:** Interactive sidebar filters, metric cards, and Plotly statistical charts.

### Phase 5: Deployment and Final Audit

- **Scope:** Optimization for Streamlit Cloud.

## 5. Engineering Standards

- **DDD:** Decoupling of logic via Service and Repository layers.
- **Efficiency:** Polars Lazy API to handle large CSV files without memory overhead.
- **Immutability:** `frozen=True` dataclasses for memory and thread safety.
- **Documentation:** Google-style docstrings in technical English.
