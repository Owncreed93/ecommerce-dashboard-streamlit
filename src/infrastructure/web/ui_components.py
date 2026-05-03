"""UI components for the Streamlit dashboard.

This module provides reusable UI elements to decouple the frontend
framework from the application orchestration.
"""

from datetime import datetime
from typing import Any

import plotly.express as px
import streamlit as st

from domain.kpi_value import KpiValue
from domain.money import Money
from domain.transaction_type import TransactionType


def render_header(country: str | None = None) -> None:
    """Renders the main dashboard header with dynamic title.

    Args:
        country: Optional country name to display in the title.
    """
    title = "Business Intelligence: Sales KPI Dashboard"
    if country:
        title = f"{title} - {country}"

    st.title(title)
    st.markdown("---")


def render_sidebar(
    unique_countries: list[str], min_date: datetime, max_date: datetime
) -> dict[str, Any]:
    """Renders the sidebar filters and returns the user selections.

    Args:
        unique_countries: List of available countries.
        min_date: Minimum available date.
        max_date: Maximum available date.

    Returns:
        A dictionary containing the selected filter values.
    """
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

    # Parse dates
    start_dt = None
    end_dt = None
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_dt, end_dt = selected_dates

    return {
        "country": selected_country,
        "start_date": start_dt,
        "end_date": end_dt,
        "trans_type": selected_trans_type,
    }


def render_kpi_grid(
    revenue: Money,
    aov: KpiValue,
    customers: int,
    returns_metrics: dict,
    trans_type: TransactionType,
) -> None:
    """Renders the 5-column KPI metric grid.

    Args:
        revenue: Money object for total revenue.
        aov: KpiValue object for AOV.
        customers: Count of active customers.
        returns_metrics: Dictionary with returns data.
        trans_type: Selected transaction type filter.
    """
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        is_return_mode = trans_type == TransactionType.RETURNS
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


def render_visualizations(
    segmentation_data: dict[str, int],
    hours_data: dict[int, int],
    trans_type: TransactionType,
) -> None:
    """Renders the Plotly charts for segmentation and peak hours.

    Args:
        segmentation_data: Data for order value segmentation.
        hours_data: Data for peak shopping hours.
        trans_type: Selected transaction type filter.
    """
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader(f"Order Value Segmentation ({trans_type.value})")
        if not segmentation_data:
            st.info("No data available for this selection.")
        else:
            fig_seg = px.pie(
                names=list(segmentation_data.keys()),
                values=list(segmentation_data.values()),
                title=f"Distribution of {trans_type.value}",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig_seg, width="stretch")

    with col_right:
        st.subheader(f"Peak Shopping Hours ({trans_type.value})")
        if not hours_data:
            st.info("No temporal patterns found for this selection.")
        else:
            is_returns = trans_type == TransactionType.RETURNS
            chart_color = "#EF553B" if is_returns else "#636EFA"

            fig_hours = px.bar(
                x=list(hours_data.keys()),
                y=list(hours_data.values()),
                labels={"x": "Hour of Day", "y": "Number of Orders"},
                title=f"Hourly {trans_type.value} Volume",
                color_discrete_sequence=[chart_color],
            )
            st.plotly_chart(fig_hours, width="stretch")
