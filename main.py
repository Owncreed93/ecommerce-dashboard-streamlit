"""Main entry point for the Streamlit dashboard.

This module initializes the application layer and renders the
interactive KPI dashboard using Streamlit and Plotly.
"""

import sys
from pathlib import Path

import streamlit as st

# Add 'src' to sys.path to allow imports from the internal layers.
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from application.kpi_service import KpiService  # noqa: E402
from infrastructure.hybrid_data_provider import HybridDataProvider  # noqa: E402
from infrastructure.polars_repository import PolarsKpiRepository  # noqa: E402
from infrastructure.web.ui_components import (  # noqa: E402
    render_header,
    render_kpi_grid,
    render_sidebar,
    render_visualizations,
)


@st.cache_resource
def get_kpi_service() -> KpiService:
    """Initializes and caches the KPI application service.

    Returns:
        A cached instance of KpiService.
    """
    # HybridDataProvider defaults to local data/data.csv if OCI_PAR_URL is missing
    data_provider = HybridDataProvider(local_path="data/data.csv")
    repo = PolarsKpiRepository(data_provider=data_provider)
    return KpiService(repository=repo)


def main() -> None:
    """Configures and runs the Streamlit dashboard."""
    st.set_page_config(
        page_title="High-Performance KPI Dashboard", page_icon="📊", layout="wide"
    )

    # 1. Service Initialization (Cached)
    service = get_kpi_service()

    # 2. Dynamic Filter Data Extraction
    # We cache this to avoid re-scanning the CSV for filter values
    @st.cache_data(ttl=3600)
    def cached_filters() -> dict:
        return service.get_filters_data()

    filters_data = cached_filters()
    unique_countries = filters_data["countries"]
    min_date, max_date = filters_data["date_range"]

    # 3. Sidebar Filters
    filters = render_sidebar(unique_countries, min_date, max_date)

    # 4. Main Dashboard Header (Dynamic Title)
    render_header(filters["country"])

    # 5. UI Skeletons / Placeholders
    # These prevent the layout from "jumping" during data processing
    kpi_placeholder = st.empty()
    viz_placeholder = st.empty()

    # 6. Data Orchestration & Rendering
    with st.spinner("Processing Business Intelligence Data..."):
        # Metric Extraction
        revenue = service.get_total_revenue(
            country=filters["country"],
            start_date=filters["start_date"],
            end_date=filters["end_date"],
            trans_type=filters["trans_type"],
        )
        aov = service.get_average_order_value(
            country=filters["country"],
            start_date=filters["start_date"],
            end_date=filters["end_date"],
            trans_type=filters["trans_type"],
        )
        customers = service.get_active_customers_count(
            country=filters["country"],
            start_date=filters["start_date"],
            end_date=filters["end_date"],
            trans_type=filters["trans_type"],
        )
        returns_metrics = service.get_returns_metrics(
            country=filters["country"],
            start_date=filters["start_date"],
            end_date=filters["end_date"],
        )

        # Render KPI Grid in the reserved placeholder
        with kpi_placeholder.container():
            render_kpi_grid(
                revenue=revenue,
                aov=aov,
                customers=customers,
                returns_metrics=returns_metrics,
                trans_type=filters["trans_type"],
            )

        # Visualization Extraction
        segmentation_data = service.get_order_segmentation(
            country=filters["country"],
            start_date=filters["start_date"],
            end_date=filters["end_date"],
            trans_type=filters["trans_type"],
        )
        hours_data = service.get_peak_hours(
            country=filters["country"],
            start_date=filters["start_date"],
            end_date=filters["end_date"],
            trans_type=filters["trans_type"],
        )

        # Render Visualizations in the reserved placeholder
        with viz_placeholder.container():
            render_visualizations(
                segmentation_data=segmentation_data,
                hours_data=hours_data,
                trans_type=filters["trans_type"],
            )


if __name__ == "__main__":
    main()
