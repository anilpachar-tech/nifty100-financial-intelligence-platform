"""
Sprint 4 - Day 22

Nifty 100 Analytics Dashboard
"""

import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Financial Intelligence Platform")

st.markdown(
"""
This dashboard provides financial analytics,
screening, peer comparison,
trend analysis and valuation
for Nifty 100 companies.
"""
)