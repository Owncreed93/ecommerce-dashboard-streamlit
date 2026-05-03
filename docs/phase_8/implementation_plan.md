# Phase 8: Dynamic Order Value Segmentation (Quantile-Based)

## 1. Objective

Replace the fixed monetary thresholds ($50 and $200) in the Order Value Segmentation metric with a dynamic, data-driven model based on statistical percentiles (25th and 75th). This ensures that customer segments are relative to the actual distribution of the dataset, providing a more accurate Business Intelligence insight across different countries and time periods.

## 2. Technical Analysis: Static vs. Dynamic Segmentation

- **The Limitation:** Fixed thresholds do not account for inflation, currency variations, or differences in market maturity (e.g., UK vs. France).
- **The Solution:** Use Polars' `quantile` function to calculate the P25 (Low bound) and P75 (High bound) values dynamically from the grouped invoice totals.

## 3. Technical Requirements

### 3.1 Domain Layer
- **Value Object:** `src/domain/segmentation_thresholds.py`
  - `@dataclass(frozen=True, slots=True)`
  - Attributes: `low_bound: Decimal`, `high_bound: Decimal`.
  - Responsibilities: Ensuring bounds are positive and logically consistent (low < high).

### 3.2 Infrastructure Layer (Repository)
- **Method:** `PolarsKpiRepository.get_revenue_quantiles()`
  - Logic: Group by `InvoiceNo`, sum total, and calculate 0.25 and 0.75 quantiles.
  - Integration: Use `@st.cache_data` to ensure these calculations (which scan the entire dataset) are efficient.

### 3.3 Application Layer (Service)
- **Refactor:** `KpiService.get_order_segmentation()`
  - Logic: Retrieve dynamic thresholds from the repository and apply them to the segmentation query.

### 3.4 Infrastructure Layer (Web)
- **UI Update:** `ui_components.py`
  - Update charts to optionally display the dynamic threshold values in the legend or as a caption for transparency.

## 4. Implementation Steps

### Step 1: Domain Modeling (TDD)
- Create unit tests for `SegmentationThresholds`.
- Implement the Value Object.

### Step 2: Data Retrieval (Infrastructure)
- Implement `get_revenue_quantiles` in `PolarsKpiRepository`.
- Add integration tests verifying quantile accuracy on a sample set.

### Step 3: Service Orchestration (Application)
- Update `KpiService` to inject dynamic thresholds into the segmentation logic.
- Update unit tests to mock the new repository method.

### Step 4: Documentation & UX
- Update `docs/business_intelligence_concepts.md` with the new percentile logic.
- Verify the final dashboard rendering.

## 5. Verification & Testing

- **Linter Check:** Run `uv run ruff check .` to ensure standard compliance.
- **Accuracy Audit:** Compare fixed results vs. dynamic results on the same dataset to ensure the transition is smooth and logical.
