# Phase 2: Data Infrastructure (Repository)

## 1. Objective

Implement the data access layer using Polars to scan and process `data/data.csv` efficiently.

## 2. Technical Requirements

- **Lazy Evaluation:** Use `polars.scan_csv` to act as a "Virtual Database".
- **Dynamic Filtering:** Implement repository methods to filter by `Country`, `Date Range`, and `Order Value` at the engine level.
- **Repository Interface:** Define an Abstract Base Class (ABC) for the repository to ensure DDD decoupling.
- **Data Cleaning:** Handle null `CustomerID` values and parse `InvoiceDate` into datetime objects.

## 3. Validation (Integration Tests)

- **Filtered Retrieval:** Verify that data returned matches specific country/date criteria.
- **Schema Integrity:** Ensure columns `Quantity`, `UnitPrice`, and `InvoiceNo` are cast to correct types (`Int64`, `Float64`).
- **Memory Efficiency:** Confirm that the repository does not load the full dataset into memory during filtering.
