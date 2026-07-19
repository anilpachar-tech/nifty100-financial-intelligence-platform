"""
Day 25
Annual Reports Dashboard

Features
--------
• Company Search
• Annual Report Browser
• KPI Cards
• Direct SQLite Connection
"""

import sqlite3
import requests
import pandas as pd
import streamlit as st

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

DB_PATH = "db/nifty100.db"

st.set_page_config(
    page_title="Annual Reports",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Annual Reports")
st.caption(
    "Browse company annual reports directly from BSE."
)

st.divider()

# ---------------------------------------------------
# Database
# ---------------------------------------------------

@st.cache_data
def load_companies():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY company_name
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data
def load_reports(company_id):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT
            year,
            Annual_Report
        FROM documents
        WHERE company_id=?
        ORDER BY year DESC
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df


# ---------------------------------------------------
# URL Checker
# ---------------------------------------------------




# ---------------------------------------------------
# Load Companies
# ---------------------------------------------------

companies = load_companies()

if companies.empty:

    st.error("No companies found.")

    st.stop()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.header("Search Company")

    selected_company = st.selectbox(
        "Company",
        companies["company_name"]
    )

# ---------------------------------------------------
# Selected Company ID
# ---------------------------------------------------

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].values[0]

# ---------------------------------------------------
# Load Reports
# ---------------------------------------------------

with st.spinner("Loading reports..."):

    reports = load_reports(company_id)

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Companies",
        companies["company_name"].nunique()
    )

with col2:

    st.metric(
        "Reports",
        len(reports)
    )

with col3:

    if len(reports):

        st.metric(
            "Latest",
            reports["year"].max()
        )

    else:

        st.metric(
            "Latest",
            "-"
        )

with col4:

    st.metric(
        "Selected Company",
        selected_company
    )

st.divider()

# ---------------------------------------------------
# Company Header
# ---------------------------------------------------

left, right = st.columns([4,1])

with left:

    st.subheader(f"🏢 {selected_company}")

    st.caption(
        "Official Annual Reports available through BSE."
    )

with right:

    st.info(
        f"{len(reports)} Reports"
    )

# ---------------------------------------------------
# Empty State
# ---------------------------------------------------

if reports.empty:

    st.warning(
        "No Annual Reports Available."
    )

    st.stop()

# ---------------------------------------------------
# Prepare Data
# ---------------------------------------------------

reports = reports.reset_index(drop=True)

reports["Status"] = reports["Annual_Report"].apply(
    lambda x:
    "Available"
    if pd.notna(x) and str(x).strip() != ""
    else "Unavailable"
)

# ---------------------------------------------------
# Report Browser
# ---------------------------------------------------

st.subheader("📚 Available Annual Reports")

for index, row in reports.iterrows():

    year = str(row["year"])

    report_url = row["Annual_Report"]

    available = True

    with st.container(border=True):

        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:

            st.markdown(f"### 📅 {year}")

        with col2:

            st.success("✅ Available")

        with col3:

            if available:

                st.link_button(
                    "📄 Open Report",
                    report_url,
                    use_container_width=True
                )

            else:

                st.button(
                    "Unavailable",
                    disabled=True,
                    use_container_width=True,
                    key=f"btn_{index}"
                )

st.divider()

# ---------------------------------------------------
# Report History
# ---------------------------------------------------

st.subheader("📈 Report Timeline")

timeline = reports.copy()

timeline["Available"] = timeline["Annual_Report"].apply(
    lambda x: 1 if pd.notna(x) and str(x).strip() != "" else 0
)

timeline = timeline.sort_values("year")

st.line_chart(
    timeline.set_index("year")["Available"],
    use_container_width=True
)

st.divider()

# ---------------------------------------------------
# Reports Table
# ---------------------------------------------------

st.subheader("📋 Reports Summary")

table = reports.copy()

table["Status"] = table["Annual_Report"].apply(
    lambda x:
    "Available"
    if pd.notna(x) and str(x).strip() != ""
    else "Unavailable"
)

st.dataframe(
    table,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------------------------------------------
# Download CSV
# ---------------------------------------------------

csv = table.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Report List",
    data=csv,
    file_name=f"{company_id}_annual_reports.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# ---------------------------------------------------
# Statistics
# ---------------------------------------------------

st.subheader("📊 Statistics")

available_count = (
    table["Status"] == "Available"
).sum()

missing_count = (
    table["Status"] == "Unavailable"
).sum()

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Available Reports",
        available_count
    )

with c2:

    st.metric(
        "Unavailable",
        missing_count
    )

with c3:

    coverage = (
        available_count /
        len(table)
    ) * 100

    st.metric(
        "Coverage",
        f"{coverage:.1f}%"
    )

st.divider()

# ---------------------------------------------------
# Recent Report
# ---------------------------------------------------

latest = reports.iloc[0]

st.subheader("⭐ Latest Annual Report")

left, right = st.columns([3, 1])

with left:

    st.write(f"**Year :** {latest['year']}")

    st.write(
        "Latest Annual Report available for this company."
    )

with right:

    st.link_button(
        "📄 View Latest",
        latest["Annual_Report"],
        use_container_width=True
    )

st.divider()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.caption(
    """
    Source: BSE Annual Reports

    Dashboard developed for the
    Nifty100 Financial Intelligence Platform.
    """
)