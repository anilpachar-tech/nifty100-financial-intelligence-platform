import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import (
    get_profile_data,
    get_company_trend,
    get_roe_roce_trend,
    get_pros_cons
)

st.title("🏢 Company Profile")

profile = get_profile_data()

companies = sorted(
    profile["company_name"]
    .dropna()
    .unique()
)

selected_company = st.selectbox(
    "Search Company",
    companies
)

company = profile[
    profile["company_name"] == selected_company
]

latest = (
    company
    .sort_values("year")
    .iloc[-1]
)

st.subheader(latest["company_name"])

col1, col2 = st.columns(2)

with col1:

    st.write(
        f"**Ticker:** {latest['id']}"
    )

    st.write(
        f"**Sector:** {latest['broad_sector']}"
    )

with col2:

    st.write(
        f"**Sub Sector:** {latest['sub_sector']}"
    )

st.markdown("### About Company")

st.write(
    latest["about_company"]
)

st.markdown("---")

logo = latest["company_logo"]

if pd.notna(logo) and str(logo).strip() != "":
    st.image(
        logo,
        width=120
    )

st.subheader("Key Financial Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

with col2:
    st.metric(
        "ROCE",
        f"{latest['return_on_capital_employed_pct']:.2f}%"
    )

with col3:
    st.metric(
        "Net Profit Margin",
        f"{latest['net_profit_margin_pct']:.2f}%"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Debt / Equity",
        round(latest["debt_to_equity"], 2)
    )

with col5:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{latest['revenue_cagr_5yr']:.2f}%"
    )

with col6:
    st.metric(
        "Free Cash Flow",
        round(latest["free_cash_flow_cr"], 2)
    )

trend = get_company_trend(
    latest["id"]
)

st.markdown("---")

st.subheader("Revenue & Net Profit (10 Years)")

fig = px.bar(
    trend,
    x="year",
    y=[
        "sales",
        "net_profit"
    ],
    barmode="group",
    title="Revenue vs Net Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

trend_ratio = get_roe_roce_trend(
    latest["id"]
)

st.markdown("---")

st.subheader("ROE vs ROCE Trend")

fig = px.line(
    trend_ratio,
    x="year",
    y=[
        "return_on_equity_pct",
        "return_on_capital_employed_pct"
    ],
    markers=True,
    title="ROE vs ROCE (10 Years)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

pros_cons = get_pros_cons(
    latest["id"]
)

st.markdown("---")
st.subheader("Pros & Cons")

col1, col2 = st.columns(2)

with col1:

    st.success("Pros")

    if not pros_cons.empty:

        for item in pros_cons["pros"]:

            if pd.notna(item):

                st.markdown(f"✅ {item}")

with col2:

    st.error("Cons")

    if not pros_cons.empty:

        for item in pros_cons["cons"]:

            if pd.notna(item):

                st.markdown(f"❌ {item}")