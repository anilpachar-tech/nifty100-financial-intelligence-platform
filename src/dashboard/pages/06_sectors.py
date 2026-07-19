import streamlit as st
import plotly.express as px

from utils.db import get_sector_analysis_data

st.title("🏭 Sector Analysis")

# =====================================================
# Load Data
# =====================================================

df = get_sector_analysis_data()

# Remove incomplete records
df = df.dropna(
    subset=[
        "broad_sector",
        "sales",
        "return_on_equity_pct",
        "market_cap_crore"
    ]
)

# =====================================================
# Sector Selector
# =====================================================

sector_list = sorted(df["broad_sector"].unique())

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

sector_df = df[
    df["broad_sector"] == selected_sector
].copy()

# =====================================================
# KPI Cards
# =====================================================

st.divider()

st.subheader("📊 Sector Median KPIs")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        "💰 Median Revenue",
        f"₹{sector_df['sales'].median():,.0f} Cr"
    )

with m2:
    st.metric(
        "📈 Median ROE",
        f"{sector_df['return_on_equity_pct'].median():.2f}%"
    )

with m3:
    st.metric(
        "🏦 Median Market Cap",
        f"₹{sector_df['market_cap_crore'].median():,.0f} Cr"
    )

# =====================================================
# Bubble Chart
# =====================================================

fig = px.scatter(

    sector_df,

    x="sales",

    y="return_on_equity_pct",

    size="market_cap_crore",

    color="sub_sector",

    hover_name="company_name",

    hover_data={
        "sales": ":,.0f",
        "market_cap_crore": ":,.0f",
        "return_on_equity_pct": ":.2f"
    },

    size_max=55,

    title=f"{selected_sector} Sector Analysis"
)

fig.update_traces(

    marker=dict(
        opacity=0.85,
        line=dict(width=1)
    ),

    hovertemplate=
    "<b>%{hovertext}</b><br><br>"
    "Revenue : ₹%{x:,.0f} Cr<br>"
    "ROE : %{y:.2f}%<br>"
    "<extra></extra>"
)

fig.update_layout(

    template="plotly_dark",

    height=700,

    xaxis_title="Revenue (₹ Crore)",

    yaxis_title="ROE (%)",

    legend_title="Sub Sector",

    hovermode="closest"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# Sector Median KPI Chart
# =====================================================

st.divider()

st.subheader("📊 Sector Median KPIs")

median_df = (
    sector_df[
        [
            "sales",
            "return_on_equity_pct",
            "market_cap_crore"
        ]
    ]
    .median()
    .reset_index()
)

median_df.columns = ["Metric", "Median Value"]

metric_names = {
    "sales": "Revenue",
    "return_on_equity_pct": "ROE (%)",
    "market_cap_crore": "Market Cap"
}

median_df["Metric"] = median_df["Metric"].map(metric_names)

fig2 = px.bar(

    median_df,

    x="Metric",

    y="Median Value",

    text_auto=".2s",

    color="Metric",

    title=f"Median KPIs - {selected_sector}"

)

fig2.update_layout(

    template="plotly_dark",

    showlegend=False,

    height=450,

    xaxis_title="",

    yaxis_title="Median Value"

)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# Top Companies Table
# =====================================================

st.divider()

st.subheader("🏆 Top Companies in Sector")

display_df = sector_df[
    [
        "company_name",
        "sub_sector",
        "sales",
        "return_on_equity_pct",
        "market_cap_crore"
    ]
].copy()

display_df = display_df.sort_values(
    by="market_cap_crore",
    ascending=False
)

display_df.columns = [
    "Company",
    "Sub Sector",
    "Revenue (₹ Cr)",
    "ROE (%)",
    "Market Cap (₹ Cr)"
]

display_df["Revenue (₹ Cr)"] = display_df["Revenue (₹ Cr)"].map(
    lambda x: f"₹{x:,.0f}"
)

display_df["ROE (%)"] = display_df["ROE (%)"].map(
    lambda x: f"{x:.2f}%"
)

display_df["Market Cap (₹ Cr)"] = display_df["Market Cap (₹ Cr)"].map(
    lambda x: f"₹{x:,.0f}"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# Sector Insights
# =====================================================

st.divider()

st.subheader("📌 Sector Insights")

highest_revenue = display_df.iloc[0]["Company"]

highest_roe = display_df.sort_values(
    "ROE (%)",
    ascending=False
).iloc[0]["Company"]

st.success(
    f"🏆 Largest Company by Market Cap: **{highest_revenue}**"
)

st.info(
    f"📈 Best ROE Company: **{highest_roe}**"
)