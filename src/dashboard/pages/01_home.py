import streamlit as st
import plotly.express as px

from utils.db import (
    get_home_data,
    get_available_years
)

st.title("🏠 Home")

# Load Data
home = get_home_data()

years = get_available_years()

# Sidebar Year Selector
selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=len(years) - 1
)

# Filter Data
if home is None or home.empty:

    st.error("No data availble.")

    st.stop()

home = home[home["year"] == selected_year].copy()

st.write(
    f"Selected Year : {selected_year}"
)

# KPI Calculations

avg_roe = round(
    home["return_on_equity_pct"].mean(),
    2
)

median_pe = round(
    home["pe"].median(),
    2
)

median_de = round(
    home["debt_to_equity"].median(),
    2
)

total_companies = (
    home["company_name"]
    .nunique()
)

median_revenue_cagr = round(
    home["revenue_cagr_5yr"].median(),
    2
)

debt_free = (
    home[
        home["debt_to_equity"] == 0
    ]["company_name"]
    .nunique()
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Average ROE",
        f"{avg_roe}%"
    )

with col2:

    st.metric(
        "Median P/E",
        median_pe
    )

with col3:

    st.metric(
        "Median D/E",
        median_de
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "Total Companies",
        total_companies
    )

with col5:

    st.metric(
        "Median Revenue CAGR (5Y)",
        f"{median_revenue_cagr}%"
    )

with col6:

    st.metric(
        "Debt-Free Companies",
        debt_free
    )

st.divider()

st.subheader("Sector Breakdown")

sector_data = (
    home.groupby("broad_sector")
    .agg(
        Companies=("company_name", "nunique")
    )
    .reset_index()
)

fig = px.pie(
    sector_data,
    names="broad_sector",
    values="Companies",
    hole=0.55,
    title="Companies by Sector"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Top 5 Companies by Composite Quality Score")

top5 = (
    home
    .sort_values(
        by="composite_quality_score",
        ascending=False
    )
    [
        [
            "id",
            "company_name",
            "broad_sector",
            "return_on_equity_pct",
            "composite_quality_score"
        ]
    ]
    .head(5)
)

top5 = top5.rename(
    columns={
        "id": "Ticker",
        "company_name": "Company",
        "broad_sector": "Sector",
        "return_on_equity_pct": "ROE (%)",
        "composite_quality_score": "Composite Score"
    }
)

st.dataframe(
    top5,
    use_container_width=True,
    hide_index=True
)