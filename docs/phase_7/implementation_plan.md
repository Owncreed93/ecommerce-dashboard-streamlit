# Phase 7: UI Layer Extraction and Performance Optimization

## 1. Objective
Refactor the application to extract UI logic into reusable components within the infrastructure layer and implement a multi-level caching strategy to mitigate cloud I/O latency, adhering to DDD and SOLID principles.

## 2. Technical Analysis: Cloud Latency vs. Caching
- **The Bottleneck:** Polars `scan_csv` over HTTP triggers Range Requests. Every Streamlit re-run repeats this I/O handshake, creating significant latency in "cold" environments.
- **Caching Tiers:**
    - **`st.cache_resource`**: Used for the `DataProvider` and `Repository` instances to maintain a persistent connection/state across sessions.
    - **`st.cache_data`**: Used for data-fetching methods in the Repository and Application layers to serialize and store the results of expensive Polars `collect()` calls.

## 3. Technical Requirements
- **Infrastructure Layer (Web):** 
    - `src/infrastructure/web/ui_components.py`: Specialized components for sidebar, metrics, and charts.
- **Performance:** 
    - Integration of `@st.cache_data` for repository queries.
    - Integration of `@st.cache_resource` for adapter initialization.
    - Implementation of `st.spinner` for user feedback during initial I/O.
- **Architectural Alignment:** Decouple Streamlit (as a primary adapter) from the business logic orchestration.

## 4. Implementation Steps

### Step 1: Documentation Update
- Refine `docs/phase_7/implementation_plan.md` with the specific caching tiers.

### Step 2: Performance Layer (Infrastructure & Application)
- Apply caching to `PolarsKpiRepository` methods (`get_unique_countries`, `get_date_range`).
- Apply caching to `KpiService` orchestration methods where applicable.
- Ensure DataProvider initialization is cached as a resource.

### Step 3: UI Component Extraction
- Create `src/infrastructure/web/ui_components.py`.
- Refactor sidebar selection logic into `render_sidebar()`.
- Refactor KPI metric display into `render_kpi_grid()`.
- Refactor Plotly visualizations into `render_visualizations()`.

### Step 4: Refactor `main.py`
- Utilize `st.spinner` during the initial data resolution.
- Clean up `main.py` to use the new cached service and UI components.

## 5. Verification & Testing
- **Linter Check:** Run `make lint` to ensure PEP 8 and project-specific rules are met.
- **Latency Audit:** Measure time-to-interactivity on Streamlit Cloud for cached vs. non-cached requests.
