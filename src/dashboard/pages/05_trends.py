import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.db import get_trend_data

st.title("📈 Trend Analysis")

# -----------------------------
# Load Data
# -----------------------------

data = get_trend_data()

# -----------------------------
# Company Search
# -----------------------------

companies = sorted(
    data["company_name"].unique()
)

selected_company = st.selectbox(
    "Select Company",
    companies
)

company_df = data[
    data["company_name"] == selected_company
].copy()

# -----------------------------
# Metric Selector
# -----------------------------

metric_map = {

    "Revenue": "sales",

    "Net Profit": "net_profit",

    "ROE": "return_on_equity_pct",

    "ROCE": "return_on_capital_employed_pct",

    "Net Profit Margin": "net_profit_margin_pct",

    "Debt / Equity": "debt_to_equity",

    "Free Cash Flow": "free_cash_flow_cr"

}

selected_metrics = st.multiselect(

    "Select up to 3 Metrics",

    options=list(metric_map.keys()),

    default=["Revenue"],

    max_selections=3

)

st.markdown("---")

# -----------------------------
# Trend Chart (Dual Y Axis)
# -----------------------------

fig = go.Figure()

left_metrics = [
    "Revenue",
    "Net Profit",
    "Free Cash Flow"
]
right_metrics = [
    "ROE",
    "ROCE",
    "Net Profit Margin",
    "Debt / Equity"
]

for metric_name in selected_metrics:

    column = metric_map[metric_name]

    plot_df = company_df[["year", column]].copy()

    plot_df = plot_df.dropna()

    plot_df = plot_df.sort_values("year")

    plot_df["yoy"] = plot_df[column].pct_change() * 100

    fig.add_trace(
        go.Scatter(
            x=plot_df["year"],
            y=plot_df[column],
            mode="lines+markers+text",
            marker=dict(size=8),
            line=dict(width=3),
            name=metric_name,
            text=[
                "" if pd.isna(x) else f"{x:.1f}%"
                for x in plot_df["yoy"]
            ],
            textposition="top center",
            yaxis="y2" if metric_name in right_metrics else "y"
        )
    )

fig.update_layout(

    title=f"{selected_company} - Financial Trends",

    xaxis=dict(
        title="Year"
    ),

    yaxis=dict(
        title="Revenue / Net Profit"
    ),

    yaxis2=dict(
        title="Financial Ratios (%)",
        overlaying="y",
        side="right"
    ),

    hovermode="x unified",

    legend=dict(
        orientation="h",
        y=1.12,
        x=0.5,
        xanchor="center"
    ),

    height=650
)

st.plotly_chart(fig, use_container_width=True)