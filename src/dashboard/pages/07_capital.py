import pandas as pd
import plotly.express as px
import streamlit as st

from utils.db import get_capital_allocation_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Capital Allocation Map",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Capital Allocation Map")
st.markdown(
    "Analyze companies based on capital allocation patterns using long-term financial performance."
)

st.divider()

# =====================================================
# CLASSIFICATION
# =====================================================

def classify_pattern(row):

    roe = float(row["roe"])
    sales = float(row["sales_growth"])
    profit = float(row["profit_growth"])

    if roe >= 25 and sales >= 15 and profit >= 15:
        return "Compounder"

    elif profit >= 20:
        return "Profit Leader"

    elif roe >= 20:
        return "Capital Efficient"

    elif sales >= 15 and profit >= 10:
        return "Growth Leader"

    elif sales >= 20:
        return "High Growth"

    elif roe >= 15:
        return "Market Performer"

    elif roe >= 8:
        return "Stable Performer"

    else:
        return "Underperformer"


# =====================================================
# LOAD DATA
# =====================================================

df = get_capital_allocation_data()

df = df.fillna(0)

df["Pattern"] = df.apply(classify_pattern, axis=1)

df = df.drop_duplicates(subset="company_name")

df["Size"] = df["roe"].clip(lower=1)

# =====================================================
# SUMMARY
# =====================================================

st.subheader("📊 Capital Allocation Summary")

pattern_counts = (
    df["Pattern"]
    .value_counts()
    .sort_values(ascending=False)
)

cols = st.columns(4)

for i, (pattern, count) in enumerate(pattern_counts.items()):
    with cols[i % 4]:
        st.metric(pattern, int(count))

st.divider()

# =====================================================
# TREEMAP
# =====================================================

st.subheader("🌳 Capital Allocation Treemap")

color_map = {
    "Compounder": "#2E8B57",
    "Profit Leader": "#FFD700",
    "Capital Efficient": "#FF8C00",
    "Growth Leader": "#8A2BE2",
    "High Growth": "#1E90FF",
    "Market Performer": "#20B2AA",
    "Stable Performer": "#808080",
    "Underperformer": "#DC143C",
}

fig = px.treemap(
    df,
    path=["Pattern", "company_name"],
    values="Size",
    color="Pattern",
    color_discrete_map=color_map,
    hover_name="company_name",
    hover_data={
        "sales_growth": ":.2f",
        "profit_growth": ":.2f",
        "roe": ":.2f",
        "Pattern": False,
        "Size": False,
        "company_name": False,
    },
)

fig.update_traces(
    textinfo="label",
    root_color="white",
)

fig.update_layout(
    margin=dict(l=5, r=5, t=20, b=5),
    height=650,
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =====================================================
# COMPANIES BY PATTERN
# =====================================================

st.subheader("📋 Companies by Pattern")

selected_pattern = st.selectbox(
    "Select Capital Allocation Pattern",
    sorted(df["Pattern"].unique()),
)

filtered_df = (
    df[df["Pattern"] == selected_pattern]
    .copy()
    .sort_values("roe", ascending=False)
)

display_df = filtered_df[
    [
        "company_name",
        "sales_growth",
        "profit_growth",
        "roe",
    ]
].copy()

display_df.columns = [
    "Company",
    "Sales Growth (%)",
    "Profit Growth (%)",
    "ROE (%)",
]

display_df["Sales Growth (%)"] = display_df["Sales Growth (%)"].round(2)
display_df["Profit Growth (%)"] = display_df["Profit Growth (%)"].round(2)
display_df["ROE (%)"] = display_df["ROE (%)"].round(2)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# =====================================================
# PATTERN STATISTICS
# =====================================================

st.subheader("📈 Pattern Statistics")

avg_sales = filtered_df["sales_growth"].mean()
avg_profit = filtered_df["profit_growth"].mean()
avg_roe = filtered_df["roe"].mean()

c1, c2, c3 = st.columns(3)

c1.metric(
    "📈 Avg Sales Growth",
    f"{avg_sales:.2f}%"
)

c2.metric(
    "💰 Avg Profit Growth",
    f"{avg_profit:.2f}%"
)

c3.metric(
    "🏦 Avg ROE",
    f"{avg_roe:.2f}%"
)

st.divider()

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("💡 Capital Allocation Insights")

most_common = pattern_counts.idxmax()
least_common = pattern_counts.idxmin()

highest_roe = df.loc[df["roe"].idxmax()]
highest_sales = df.loc[df["sales_growth"].idxmax()]

left, right = st.columns(2)

with left:

    st.success(
        f"""
### 🏆 Most Common Pattern

**{most_common}**

Companies : **{pattern_counts.max()}**
"""
    )

    st.info(
        f"""
### 🚀 Highest Sales Growth

**{highest_sales['company_name']}**

Growth : **{highest_sales['sales_growth']:.2f}%**
"""
    )

with right:

    st.warning(
        f"""
### ⭐ Highest ROE Company

**{highest_roe['company_name']}**

ROE : **{highest_roe['roe']:.2f}%**
"""
    )

    st.error(
        f"""
### 📉 Least Common Pattern

**{least_common}**

Companies : **{pattern_counts.min()}**
"""
    )

st.divider()

# =====================================================
# DASHBOARD SUMMARY
# =====================================================

st.subheader("📊 Dashboard Summary")

s1, s2, s3, s4 = st.columns(4)

s1.metric(
    "Companies",
    int(df["company_name"].nunique()),
)

s2.metric(
    "Patterns",
    int(df["Pattern"].nunique()),
)

s3.metric(
    "Average ROE",
    f"{df['roe'].mean():.2f}%"
)

s4.metric(
    "Average Sales Growth",
    f"{df['sales_growth'].mean():.2f}%"
)

st.divider()

# =====================================================
# DOWNLOAD
# =====================================================

csv = display_df.to_csv(index=False)

st.download_button(
    label="📥 Download Company List",
    data=csv,
    file_name="capital_allocation_companies.csv",
    mime="text/csv",
)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Capital Allocation patterns are derived using Revenue CAGR, PAT CAGR and Return on Equity (ROE) from the latest available financial data."
)