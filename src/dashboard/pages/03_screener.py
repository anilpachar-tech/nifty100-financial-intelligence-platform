import streamlit as st

from utils.db import get_screener_data

# -----------------------------
# Default Filter Values
# -----------------------------

DEFAULT_FILTERS = {

    "roe_min": 15.0,
    "de_max": 2.0,
    "fcf_min": 0.0,
    "revenue_cagr_min": 10.0,
    "pat_cagr_min": 10.0,
    "opm_min": 10.0,
    "pe_max": 50.0,
    "pb_max": 10.0,
    "dividend_min": 0.0,
    "icr_min": 1.5

}

for key, value in DEFAULT_FILTERS.items():

    if key not in st.session_state:

        st.session_state[key] = value

def apply_preset(name):

    if name == "quality":

        st.session_state.roe_min = 15.0
        st.session_state.de_max = 1.0
        st.session_state.fcf_min = 0.0
        st.session_state.revenue_cagr_min = 10.0

    elif name == "value":

        st.session_state.pe_max = 20.0
        st.session_state.pb_max = 3.0
        st.session_state.de_max = 2.0
        st.session_state.dividend_min = 1.0

    elif name == "growth":

        st.session_state.pat_cagr_min = 20.0
        st.session_state.revenue_cagr_min = 15.0
        st.session_state.de_max = 2.0

    elif name == "dividend":

        st.session_state.dividend_min = 2.0
        st.session_state.fcf_min = 0.0

    elif name == "debtfree":

        st.session_state.de_max = 0.0
        st.session_state.roe_min = 12.0

    elif name == "turnaround":

        st.session_state.revenue_cagr_min = 10.0
        st.session_state.fcf_min = 0.0


st.title("🔍 Stock Screener")

data = get_screener_data()

st.sidebar.header("Filters")

st.sidebar.subheader("Presets")

if st.sidebar.button("🏆 Quality"):
    apply_preset("quality")
    st.rerun()

if st.sidebar.button("💰 Value"):
    apply_preset("value")
    st.rerun()

if st.sidebar.button("📈 Growth"):
    apply_preset("growth")
    st.rerun()

if st.sidebar.button("💵 Dividend"):
    apply_preset("dividend")
    st.rerun()

if st.sidebar.button("✅ Debt Free"):
    apply_preset("debtfree")
    st.rerun()

if st.sidebar.button("🚀 Turnaround"):
    apply_preset("turnaround")
    st.rerun()

if st.sidebar.button("🔄 Reset Filters"):
    for key, value in DEFAULT_FILTERS.items():
        st.session_state[key] = value

    st.rerun()

roe_min = st.sidebar.slider(
    "ROE Min (%)",
    0.0,
    100.0,
    key="roe_min"
)

de_max = st.sidebar.slider(
    "Debt / Equity Max",
    0.0,
    10.0,
    key="de_max"
)

fcf_min = st.sidebar.number_input(
    "FCF Min",
    key="fcf_min"
)

revenue_cagr_min = st.sidebar.slider(
    "Revenue CAGR 5Y Min (%)",
    -50.0,
    100.0,
    key="revenue_cagr_min"
)

pat_cagr_min = st.sidebar.slider(
    "PAT CAGR 5Y Min (%)",
    -50.0,
    100.0,
    key="pat_cagr_min"
)

opm_min = st.sidebar.slider(
    "Operating Profit Margin Min (%)",
    0.0,
    100.0,
    key="opm_min"
)

pe_max = st.sidebar.slider(
    "P/E Max",
    0.0,
    200.0,
    key="pe_max"
)

pb_max = st.sidebar.slider(
    "P/B Max",
    0.0,
    50.0,
    key="pb_max"
)

dividend_min = st.sidebar.slider(
    "Dividend Yield Min (%)",
    0.0,
    20.0,
    key="dividend_min"
)

icr_min = st.sidebar.slider(
    "Interest Coverage Min",
    0.0,
    100.0,
    key="icr_min"
)

filtered = data.copy()

filtered = filtered[
    (filtered["return_on_equity_pct"] >= roe_min)
    &
    (filtered["debt_to_equity"] <= de_max)
    &
    (filtered["free_cash_flow_cr"] >= fcf_min)
    &
    (filtered["revenue_cagr_5yr"] >= revenue_cagr_min)
    &
    (filtered["pat_cagr_5yr"] >= pat_cagr_min)
    &
    (filtered["operating_profit_margin_pct"] >= opm_min)
    &
    (filtered["pe"] <= pe_max)
    &
    (filtered["pb"] <= pb_max)
    &
    (filtered["dividend_yield"] >= dividend_min)
    &
    (
        (filtered["interest_coverage"] >= icr_min)
        |
        (filtered["interest_coverage"].isna())
    )
]

st.subheader(f"📊 Results ({len(filtered)} Companies)")

st.caption(
    f"Showing {len(filtered)} of {len(data)} records"
)

st.dataframe(
    filtered[
        [
            "id",
            "company_name",
            "broad_sector",
            "composite_quality_score",
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "operating_profit_margin_pct",
            "pe",
            "pb",
            "dividend_yield"
        ]
    ],
    use_container_width=True
)

csv = filtered[
    [
        "id",
        "company_name",
        "broad_sector",
        "composite_quality_score",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "operating_profit_margin_pct",
        "pe",
        "pb",
        "dividend_yield"
    ]
].to_csv(index=False)

filtered = filtered.sort_values(
    by="composite_quality_score",
    ascending=False
)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="screener_results.csv",
    mime="text/csv"
)