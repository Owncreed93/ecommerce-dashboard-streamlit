"""Main entry point for the Streamlit dashboard.

This module initializes the application layer and renders the
interactive KPI dashboard using Streamlit and Plotly.
"""

import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

# Add 'src' to sys.path to allow imports from the internal layers.
# This is required for deployment on Streamlit Cloud.
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from application.kpi_service import KpiService  # noqa: E402
from domain.transaction_type import TransactionType  # noqa: E402
from infrastructure.hybrid_data_provider import HybridDataProvider  # noqa: E402
from infrastructure.polars_repository import PolarsKpiRepository  # noqa: E402


def main() -> None:
    """Configures and runs the Streamlit dashboard."""
    st.set_page_config(
        page_title="High-Performance KPI Dashboard", page_icon="📊", layout="wide"
    )

    # 1. Infrastructure and Service Initialization
    # HybridDataProvider defaults to local data/data.csv if OCI_PAR_URL is missing
    data_provider = HybridDataProvider(local_path="data/data.csv")
    repo = PolarsKpiRepository(data_provider=data_provider)
    service = KpiService(repository=repo)

    # 2. Dynamic Filter Data Extraction
    filters_data = service.get_filters_data()
    unique_countries = filters_data["countries"]
    min_date, max_date = filters_data["date_range"]

    # 3. Sidebar Filters
    st.sidebar.header("Dashboard Filters")

    selected_country = st.sidebar.selectbox(
        "Select Country",
        options=[None] + unique_countries,
        index=0,
        format_func=lambda x: "All Countries" if x is None else x,
    )

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    selected_trans_type = st.sidebar.radio(
        "Order Status Filter",
        options=list(TransactionType),
        format_func=lambda x: x.value,
    )

    # 4. Main Dashboard Header
    st.title("Business Intelligence: Sales KPI Dashboard")
    st.markdown("---")

    # 5. Strategic Metric Cards
    # Streamlit date_input returns a tuple (start, end)
    start_dt = None
    end_dt = None
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_dt, end_dt = selected_dates

    # Use the selected transaction type and dates for metrics
    revenue = service.get_total_revenue(
        country=selected_country,
        start_date=start_dt,
        end_date=end_dt,
        trans_type=selected_trans_type,
    )
    aov = service.get_average_order_value(
        country=selected_country,
        start_date=start_dt,
        end_date=end_dt,
        trans_type=selected_trans_type,
    )
    customers = service.get_active_customers_count(
        country=selected_country,
        start_date=start_dt,
        end_date=end_dt,
        trans_type=selected_trans_type,
    )
    returns_metrics = service.get_returns_metrics(
        country=selected_country, start_date=start_dt, end_date=end_dt
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        is_return_mode = selected_trans_type == TransactionType.RETURNS
        label = "Returns Value" if is_return_mode else "Total Revenue"
        st.metric(label, f"{revenue.amount:,.2f} {revenue.currency}")
    with col2:
        st.metric("Avg Order Value", aov.format())
    with col3:
        st.metric("Active Customers", f"{customers:,}")
    with col4:
        ret_val = returns_metrics["total_returns"].amount
        ret_curr = returns_metrics["total_returns"].currency
        st.metric("Total Returns", f"{ret_val:,.2f} {ret_curr}", delta_color="inverse")
    with col5:
        st.metric("Return Rate", returns_metrics["return_rate"].format())

    st.markdown("---")

    # 6. Advanced Visualizations
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader(f"Order Value Segmentation ({selected_trans_type.value})")
        segmentation_data = service.get_order_segmentation(
            country=selected_country,
            start_date=start_dt,
            end_date=end_dt,
            trans_type=selected_trans_type,
        )

        if not segmentation_data:
            st.info("No data available for this selection.")
        else:
            fig_seg = px.pie(
                names=list(segmentation_data.keys()),
                values=list(segmentation_data.values()),
                title=f"Distribution of {selected_trans_type.value}",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig_seg, use_container_width=True)

    with col_right:
        st.subheader(f"Peak Shopping Hours ({selected_trans_type.value})")
        hours_data = service.get_peak_hours(
            country=selected_country,
            start_date=start_dt,
            end_date=end_dt,
            trans_type=selected_trans_type,
        )

        if not hours_data:
            st.info("No temporal patterns found for this selection.")
        else:
            is_returns = selected_trans_type == TransactionType.RETURNS
            chart_color = "#EF553B" if is_returns else "#636EFA"

            fig_hours = px.bar(
                x=list(hours_data.keys()),
                y=list(hours_data.values()),
                labels={"x": "Hour of Day", "y": "Number of Orders"},
                title=f"Hourly {selected_trans_type.value} Volume",
                color_discrete_sequence=[chart_color],
            )
            st.plotly_chart(fig_hours, use_container_width=True)


if __name__ == "__main__":
    main()
