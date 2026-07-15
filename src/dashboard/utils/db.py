"""
Sprint 4 - Day 22

Dashboard Database Utilities
"""

import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


@st.cache_data(ttl=600)
def get_companies():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        ORDER BY company_name
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios(
    ticker,
    year=None
):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    """

    params = [ticker]

    if year is not None:

        query += """
        AND year = ?
        """

        params.append(year)

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        ORDER BY year
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sectors():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM sectors
        ORDER BY sector_name
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_groups
        WHERE peer_group_name = ?
        """,
        conn,
        params=[group_name]
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = sqlite3.connect(DB_PATH)

    try:

        df = pd.read_sql(
            """
            SELECT *
            FROM valuation_summary
            WHERE company_id = ?
            """,
            conn,
            params=[ticker]
        )

    except Exception:

        df = pd.DataFrame()

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_home_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        f.year,
        f.return_on_equity_pct,
        f.return_on_capital_employed_pct,
        f.debt_to_equity,
        f.pe,
        f.revenue_cagr_5yr,
        f.composite_quality_score

    FROM financial_ratios f

    JOIN companies c
    ON f.company_id = c.id

    LEFT JOIN sectors s
    ON c.id = s.company_id
    """
    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_available_years():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT DISTINCT year
        FROM financial_ratios
        """,
        conn
    )

    conn.close()

    month_order = {
        "Mar": 3,
        "Jun": 6,
        "Sep": 9,
        "Dec": 12
    }

    years = sorted(
        df["year"].tolist(),
        key=lambda x: (
            int(x.split()[1]),
            month_order.get(x.split()[0], 0)
        )
    )

    return years

@st.cache_data(ttl=600)
def get_profile_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        c.id,
        c.company_name,
        c.company_logo,
        c.about_company,

        s.broad_sector,
        s.sub_sector,

        f.year,
        f.return_on_equity_pct,
        f.return_on_capital_employed_pct,
        f.net_profit_margin_pct,
        f.debt_to_equity,
        f.revenue_cagr_5yr,
        f.free_cash_flow_cr

    FROM financial_ratios f

    INNER JOIN companies c
        ON f.company_id = c.id

    LEFT JOIN sectors s
        ON c.id = s.company_id
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_company_trend(company_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        company_id,
        year,
        sales,
        net_profit
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_roe_roce_trend(company_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        return_on_capital_employed_pct
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    df = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_pros_cons(company_id):

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        pros,
        cons
    FROM prosandcons
    WHERE company_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    return df
