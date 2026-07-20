import os
import sqlite3
import pandas as pd
import numpy as np


DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "output"


def get_connection():
    """Create SQLite connection."""
    return sqlite3.connect(DB_PATH)


def load_latest_data():
    """
    Load latest valuation data by joining
    companies, financial_ratios,
    market_cap and sectors.
    """

    conn = get_connection()

    query = """
    WITH latest_ratios AS (
        SELECT *
        FROM financial_ratios fr
        WHERE year = (
            SELECT MAX(year)
            FROM financial_ratios
            WHERE company_id = fr.company_id
        )
    ),

    latest_market AS (
        SELECT *
        FROM market_cap mc
        WHERE year = (
            SELECT MAX(year)
            FROM market_cap
            WHERE company_id = mc.company_id
        )
    )

    SELECT
        c.id AS company_id,
        c.company_name,

        s.broad_sector,

        lr.year,

        lr.pe,
        lr.pb,

        lm.market_cap_crore,
        lm.ev_ebitda,

        lr.free_cash_flow_cr,
        lr.revenue_cagr_5yr,
        lr.composite_quality_score

    FROM companies c

    LEFT JOIN latest_ratios lr
        ON c.id = lr.company_id

    LEFT JOIN latest_market lm
        ON c.id = lm.company_id

    LEFT JOIN sectors s
        ON c.id = s.company_id

    ORDER BY c.company_name;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def load_market_history():
    """
    Load historical PE data
    required for 5-Year Median PE.
    """

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        pe_ratio
    FROM market_cap
    WHERE pe_ratio IS NOT NULL
    """

    history = pd.read_sql(query, conn)

    conn.close()

    return history

def calculate_fcf_yield(df):
    """
    Calculate Free Cash Flow Yield (%)
    """

    df = df.copy()

    df["FCF_yield_pct"] = (
        df["free_cash_flow_cr"] /
        df["market_cap_crore"]
    ) * 100

    df["FCF_yield_pct"] = df["FCF_yield_pct"].round(2)

    return df


def calculate_5yr_median_pe(history):
    """
    Calculate 5-Year Median PE
    """

    median_pe = (
        history.groupby("company_id")["pe_ratio"]
        .median()
        .reset_index()
        .rename(columns={"pe_ratio": "5yr_median_PE"})
    )

    return median_pe


def calculate_sector_median(df):
    """
    Calculate sector median PE
    """

    sector_median = (
        df.groupby("broad_sector")["pe"]
        .median()
        .reset_index()
        .rename(columns={"pe": "sector_median_pe"})
    )

    return sector_median


def apply_valuation_flags(df, median_pe, sector_median):
    """
    Merge calculated metrics and assign valuation flags.
    """

    df = df.merge(
        median_pe,
        on="company_id",
        how="left"
    )

    df = df.merge(
        sector_median,
        on="broad_sector",
        how="left"
    )

    df["PE_vs_sector_median_pct"] = (
        (
            df["pe"] - df["sector_median_pe"]
        )
        / df["sector_median_pe"]
    ) * 100

    df["PE_vs_sector_median_pct"] = (
        df["PE_vs_sector_median_pct"]
        .round(2)
    )

    conditions = [
        df["pe"] > df["sector_median_pe"] * 1.5,
        df["pe"] < df["sector_median_pe"] * 0.7
    ]

    choices = [
        "Caution",
        "Discount"
    ]

    df["flag"] = np.select(
        conditions,
        choices,
        default="Fair"
    )

    return df

def save_outputs(df):
    """
    Save valuation summary and flags to output folder.
    """

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    valuation_summary = df[
        [
            "company_id",
            "company_name",
            "broad_sector",
            "pe",
            "pb",
            "ev_ebitda",
            "FCF_yield_pct",
            "5yr_median_PE",
            "PE_vs_sector_median_pct",
            "flag"
        ]
    ].copy()

    valuation_summary.rename(
        columns={
            "broad_sector": "sector",
            "pe": "P/E",
            "pb": "P/B",
            "ev_ebitda": "EV/EBITDA"
        },
        inplace=True
    )

    valuation_flags = valuation_summary[
        valuation_summary["flag"].isin(
            ["Caution", "Discount"]
        )
    ].copy()

    summary_path = os.path.join(
        OUTPUT_DIR,
        "valuation_summary.xlsx"
    )

    flags_path = os.path.join(
        OUTPUT_DIR,
        "valuation_flags.csv"
    )

    valuation_summary.to_excel(
        summary_path,
        index=False
    )

    valuation_flags.to_csv(
        flags_path,
        index=False
    )

    print("\n" + "=" * 60)
    print("VALUATION MODULE COMPLETED")
    print("=" * 60)
    print(f"Total Companies : {len(valuation_summary)}")
    print(f"Flagged Companies : {len(valuation_flags)}")
    print(f"Summary File : {summary_path}")
    print(f"Flags File : {flags_path}")
    print("=" * 60)


def main():

    print("Loading latest valuation data...")

    df = load_latest_data()

    print("Loading market history...")

    history = load_market_history()

    print("Calculating FCF Yield...")

    df = calculate_fcf_yield(df)

    print("Calculating 5-Year Median PE...")

    median_pe = calculate_5yr_median_pe(history)

    print("Calculating Sector Median PE...")

    sector_median = calculate_sector_median(df)

    print("Applying valuation flags...")

    df = apply_valuation_flags(
        df,
        median_pe,
        sector_median
    )

    print("Saving output files...")

    save_outputs(df)

    print("\nDone!")


if __name__ == "__main__":
    main()