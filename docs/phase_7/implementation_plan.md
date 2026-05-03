# Phase 7: UI Layer Extraction, Performance Optimization & UX Refinement

## 1. Objective

Refactor the application to extract UI logic into reusable components within the infrastructure layer, implement a multi-level caching strategy to mitigate cloud I/O latency, and resolve critical UX/data consistency issues (Dynamic Titles, Histogram Accuracy, and Smooth Transitions).

## 2. Technical Analysis: Cloud Latency vs. Caching

- **The Bottleneck:** Polars `scan_csv` over HTTP triggers Range Requests. Every Streamlit re-run repeats this I/O handshake, creating significant latency.
- **Caching Tiers:**
  - **`st.cache_resource`**: Used for `DataProvider` and `Repository` instances.
  - **`st.cache_data`**: Used for data-fetching methods to serialize Polars `collect()` results.

## 3. Technical Requirements

- **Infrastructure Layer (Web):**
  - `src/infrastructure/web/ui_components.py`: Components for header, sidebar, metrics, and charts.
- **Performance & UX:**
  - Integration of `@st.cache_data` and `@st.cache_resource`.
  - Implementation of **UI Skeletons/Placeholders** using `st.empty()` to prevent layout shifts.
  - **Dynamic Dashboard Title**: Appending the selected country name to the main header.
- **Data Integrity:**
  - **Histogram Fix**: Ensure unique `InvoiceNo` counting in peak hours distribution.

## 4. Implementation Steps

### Step 1: Logic & Data Integrity (Application Layer)

- Update `KpiService.get_peak_hours` to apply `.unique("InvoiceNo")` before grouping by hour.
- Add unit tests to verify unique invoice counting per hour.

### Step 2: UI Component Extraction (Infrastructure Layer)

- Create `src/infrastructure/web/ui_components.py`.
- `render_header(country: str | None)`: Logic for dynamic title.
- `render_sidebar(...)`: Sidebar filter encapsulation.
- `render_kpi_grid(...)`: Metric cards with placeholder support.
- `render_visualizations(...)`: Plotly charts with placeholder support.

### Step 3: Performance & UX Refinement (Infrastructure & Main)

- Apply caching decorators to `PolarsKpiRepository` and `KpiService`.
- Refactor `main.py` to use `st.empty()` placeholders for each major section (Metrics, Charts).
- Replace `st.spinner` with targeted loading states within placeholders to ensure smooth transitions.

## 5. Verification & Testing

- **Linter Check:** Run `make lint` (Ruff) to ensure project standards.
- **Manual UX Audit:** Verify dynamic title behavior and transition smoothness (no "jumping" UI).
- **Accuracy Check:** Validate histogram bars against a known subset of data (1 invoice = 1 count).
