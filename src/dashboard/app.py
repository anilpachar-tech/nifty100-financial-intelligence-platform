import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

home = st.Page(
    "pages/01_home.py",
    title="Home",
    icon="🏠"
)

profile = st.Page(
    "pages/02_profile.py",
    title="Company Profile",
    icon="🏢"
)

screener = st.Page(
    "pages/03_screener.py",
    title="Stock Screener",
    icon="🔍"
)

peers = st.Page(
    "pages/04_peers.py",
    title="Peer Comparison",
    icon="👥"
)

trends = st.Page(
    "pages/05_trends.py",
    title="Trend Analysis",
    icon="📈"
)

sectors = st.Page(
    "pages/06_sectors.py",
    title="Sector Analysis",
    icon="🏭"
)

capital = st.Page(
    "pages/07_capital.py",
    title="Capital Allocation",
    icon="💰"
)

reports = st.Page(
    "pages/08_reports.py",
    title="Annual Reports",
    icon="📄"
)

pg = st.navigation(
    [
        home,
        profile,
        screener,
        peers,
        trends,
        sectors,
        capital,
        reports
    ]
)

pg.run()