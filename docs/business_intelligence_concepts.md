# Business Intelligence Concepts and Metric Specifications

## 1. Executive Summary

This document defines the analytical framework and the mathematical logic applied to the KPI Dashboard. The system leverages Domain-Driven Design (DDD) to ensure that business rules are decoupled from technical infrastructure, providing a high-precision view of organizational performance.

## 2. Core Financial Metrics

### 2.1 Net Revenue

The system calculates Net Revenue as the primary indicator of financial health. Unlike Gross Volume, which sums all transactions regardless of direction, Net Revenue accounts for the actual capital retained after cancellations.

- **Formula:** Total Sales - Total Returns.
- **Logic:** Sales transactions (positive quantity, no cancellation prefix) are aggregated with returns (negative quantity, cancellation prefix 'C').
- **Business Value:** Provides a realistic view of profitability and cash flow.

### 2.2 Average Order Value (AOV)

AOV measures the average amount of capital generated per unique transaction.

- **Formula:** Net Revenue / Unique Invoice Count.
- **Logic:** The system ensures that multiple line items belonging to the same InvoiceNo are treated as a single transaction unit.
- **Business Value:** Identifies customer purchasing power and helps in evaluating pricing strategies.

## 3. Statistical Distribution Metrics

### 3.1 Order Value Segmentation (Dynamic Quantile Model)

This metric categorizes transactions into qualitative buckets based on their relative monetary value within the specific data distribution of a filtered context.

- **Dynamic Benchmarking:** Instead of using fixed monetary thresholds (e.g., $50), the system calculates the distribution of all unique invoices.
- **Segmentation Tiers:**
  - **Low Value (P25):** Transactions below the 25th percentile of the current distribution.
  - **Mid Value:** Transactions between the 25th and 75th percentile (Interquartile Range).
  - **High Value (P75):** Transactions above the 75th percentile (Premium/Wholesale tier).
- **Mathematical Rationale:** Using quantiles makes the dashboard resilient to inflation, currency changes, and regional economic disparities.
- **Business Value:** Enables context-aware targeted marketing and identifies high-value customers relative to their local market.

### 3.2 Peak Shopping Hours (Temporal Analysis)

Analyzes transaction density over a 24-hour cycle to identify peak operational windows.

- **Calculation Logic:** Aggregation of unique InvoiceNo counts grouped by the hour component of the InvoiceDate.
- **Constraint:** To maintain data integrity, an invoice is counted only once, even if it contains multiple product lines or is partially returned at the same hour.
- **Business Value:** Optimizes staffing levels and server resource allocation for web-based retail.

## 4. Operational Metrics

### 4.1 Active Customer Base

The count of unique customers who have performed at least one transaction within the filtered period.

- **Identifier:** CustomerID.
- **Business Value:** Measures customer retention and market reach.

### 4.2 Return Rate

The ratio of returned value against gross sales.

- **Formula:** (Total Returns Value / Gross Sales Value) * 100.
- **Business Value:** Acts as a quality control indicator and identifies potential issues with product descriptions or logistics.

## 5. Architectural Implementation

All metrics are orchestrated within the Application Layer (KpiService), ensuring that:

1. **Precision:** Financial calculations use Decimal types to avoid binary floating-point errors.
2. **Efficiency:** Data processing is offloaded to the Polars engine using Lazy Evaluation for performance.
3. **Immutability:** Results are returned as Value Objects to prevent state corruption during UI rendering.
