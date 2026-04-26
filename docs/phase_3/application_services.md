# Phase 3: Application Services (KPI Logic)

## 1. Objective

Orchestrate the calculation of business KPIs and statistical distributions using Domain Objects.

## 2. Technical Requirements

- **Strategic KPI Implementation:**
  - `Total Revenue`: Summation with `Decimal` precision.
  - `Average Order Value (AOV)`: Dynamic ratio calculation.
  - `Active Customer Base`: Unique customer tracking.
- **Statistical Logic:**
  - `Order Value Segmentation`: Binning logic for High/Mid/Low value orders.
  - `Peak Shopping Hours`: Hour extraction and grouping by country.
  - `Revenue Contribution %`: Calculation of market share per category.
  - `Sales Velocity`: Trend calculation over time.
- **Decoupling:** Services must depend on the Repository abstraction, not the Polars implementation.

## 3. Validation (Unit Tests)

- **Calculation Precision:** Use controlled mock data to verify `Decimal` arithmetic in revenue.
- **Segmentation Integrity:** Ensure binned categories correctly capture boundary values.
- **Edge Cases:** Handle datasets with single entries or inconsistent timestamps.
