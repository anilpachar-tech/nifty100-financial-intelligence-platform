import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.db import (
    get_peer_groups,
    get_latest_peer_data,
)

from utils.db import get_peer_average

st.title("👥 Peer Comparison")

# ------------------------------------
# Peer Group
# ------------------------------------

groups = get_peer_groups()

selected_group = st.selectbox(

    "Select Peer Group",

    groups["peer_group_name"]

)

peer_data = get_latest_peer_data(
    selected_group
)

# ------------------------------------
# Company Dropdown
# ------------------------------------

selected_company = st.selectbox(

    "Select Company",

    peer_data["company_name"]

)

company = peer_data[
    peer_data["company_name"] == selected_company
]

latest = company.iloc[0]

st.markdown("---")

# ------------------------------------
# Company Card
# ------------------------------------

st.subheader(latest["company_name"])

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "ROE",
        round(
            latest["return_on_equity_pct"],
            2
        )
    )

    st.metric(
        "ROCE",
        round(
            latest["return_on_capital_employed_pct"],
            2
        )
    )

    st.metric(
        "Net Profit Margin",
        round(
            latest["net_profit_margin_pct"],
            2
        )
    )

with col2:

    st.metric(
        "Debt / Equity",
        round(
            latest["debt_to_equity"],
            2
        )
    )

    st.metric(
        "Revenue CAGR",
        round(
            latest["revenue_cagr_5yr"],
            2
        )
    )

    st.metric(
        "PAT CAGR",
        round(
            latest["pat_cagr_5yr"],
            2
        )
    )

st.markdown("---")

st.subheader("📊 Company vs Peer Average")

peer_avg = get_peer_average(selected_group)

categories = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "Revenue CAGR",
    "PAT CAGR",
    "Quality"
]

def normalize(company, peer):

    values = []

    for c, p in zip(company, peer):

        mx = max(c, p)

        if mx == 0:
            values.append((50, 50))
        else:
            values.append(
                (
                    (c / mx) * 100,
                    (p / mx) * 100
                )
            )

    company_norm = [v[0] for v in values]
    peer_norm = [v[1] for v in values]

    return company_norm, peer_norm

company_values = [
    latest["return_on_equity_pct"],
    latest["return_on_capital_employed_pct"],
    latest["net_profit_margin_pct"],
    latest["debt_to_equity"],
    latest["free_cash_flow_cr"],
    latest["revenue_cagr_5yr"],
    latest["pat_cagr_5yr"],
    latest["composite_quality_score"]
]

peer_values = [
    peer_avg["return_on_equity_pct"],
    peer_avg["return_on_capital_employed_pct"],
    peer_avg["net_profit_margin_pct"],
    peer_avg["debt_to_equity"],
    peer_avg["free_cash_flow_cr"],
    peer_avg["revenue_cagr_5yr"],
    peer_avg["pat_cagr_5yr"],
    peer_avg["composite_quality_score"]
]

company_values, peer_values = normalize(
    company_values,
    peer_values
)

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=categories,
        fill="toself",
        name=latest["company_name"]
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=categories,
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

def highlight_benchmark(row):

    if row["is_benchmark"] == 1:
        return ["background-color:#1f8a4c; color:white"] * len(row)

    return [""] * len(row)

st.subheader("Peer Group Companies")

styled_df = peer_data.style.apply(
    highlight_benchmark,
    axis=1
)

display_df = peer_data.copy()

display_df["Benchmark"] = display_df["is_benchmark"].apply(
    lambda x: "🏆" if str(x).strip() == "1" else ""
)

display_df = display_df.drop(columns=["is_benchmark"])

display_df = display_df[
    [
        "Benchmark",
        "company_name",
        "peer_group_name",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "composite_quality_score"
    ]
]

display_df = display_df.rename(
    columns={
        "company_name": "Company",
        "peer_group_name": "Peer Group",
        "return_on_equity_pct": "ROE",
        "return_on_capital_employed_pct": "ROCE",
        "net_profit_margin_pct": "Net Profit Margin",
        "debt_to_equity": "Debt / Equity",
        "revenue_cagr_5yr": "Revenue CAGR (5Y)",
        "pat_cagr_5yr": "PAT CAGR (5Y)",
        "composite_quality_score": "Quality Score"
    }
)

st.dataframe(
    display_df,
    use_container_width=True
)