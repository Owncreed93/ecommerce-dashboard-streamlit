# Phase 4: Streamlit Interface

## 1. Objective

Develop a professional, reactive dashboard with interactive filters and advanced visualizations.

## 2. Technical Requirements

- **Sidebar State Management:** Implement filters for `Country`, `Date Range`, and `Order Value Thresholds`.
- **Strategic Metric Cards:** Display `Total Revenue`, `AOV`, and `Customers` using `st.metric`.
- **Advanced Visualizations:**
  - **Plotly Histogram:** For Order Value Segmentation.
  - **Plotly Heatmap/Bar Chart:** For Peak Shopping Hours by Country.
  - **Plotly Pie/Donut:** For Revenue Contribution %.
  - **Plotly Line Chart:** For Sales Velocity trends.
- **Performance:** Use Streamlit caching to prevent redundant data processing.

## Phase 4.5: Returns Analytics

### 1. Objective
Identify and visualize patterns in product returns (negative quantities) to optimize business operations and inventory management.

### 2. Technical Requirements
- **Returns Metrics:**
  - `Total Returns Value`: Sum of absolute values of negative transactions.
  - `Return Rate`: Ratio of Returns Value to Gross Sales.
  - `Returns by Country/Hour`: Distribution analysis for negative transactions.
- **UI Integration:**
  - Dedicated "Returns" section with color-coded alerts (Ley de Von Restorff).
  - Toggle filter to switch between "Gross Sales", "Returns", and "Net Total".

## Phase 4.6: Domain Integrity and Identifier Validation

### 1. Objective
Encapsulate business logic for identifiers within specialized Value Objects to ensure data integrity and formalize the detection of cancellations.

### 2. Technical Requirements
- **Value Objects:**
  - `InvoiceIdentifier`: Handles alphanumeric validation and provides an `is_cancellation` property based on the 'C' prefix.
  - `CustomerIdentifier`: Validates customer ID format and handles missing/null values consistently.
- **Business Rule Enforcement:**
  - Move cancellation detection logic from the Infrastructure/Application layer into the Domain layer.
  - Ensure all identifiers are immutable and memory-optimized (frozen dataclasses with slots).

## 3. Validation (Integration / E2E)

- **Filter Reactivity:** Verify that changing a sidebar filter updates all related charts immediately.
- **Cross-browser Compatibility:** Ensure Plotly charts render correctly on various viewport sizes (Mobile First).
