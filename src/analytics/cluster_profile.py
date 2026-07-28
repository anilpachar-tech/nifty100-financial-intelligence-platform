import sqlite3
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

CLUSTER_FILE = OUTPUT_DIR / "cluster_labels.csv"

OUTPUT_DIR.mkdir(exist_ok=True)


# ==========================================================
# Database Connection
# ==========================================================


def connect_database():
    return sqlite3.connect(DATABASE_PATH)


# ==========================================================
# Load Cluster Labels
# ==========================================================


def load_cluster_labels():

    df = pd.read_csv(CLUSTER_FILE)

    return df


# ==========================================================
# Load Financial Data
# ==========================================================


def load_financial_data():

    conn = connect_database()

    query = """
    SELECT

        c.id AS company_id,
        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.revenue_cagr_5yr,
        fr.free_cash_flow_cr,
        fr.operating_profit_margin_pct

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN (

        SELECT *
        FROM financial_ratios f1

        WHERE rowid IN (

            SELECT rowid
            FROM financial_ratios f2

            WHERE f2.company_id = f1.company_id

            ORDER BY year DESC

            LIMIT 1

        )

    ) fr

        ON c.id = fr.company_id

    ORDER BY c.id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ==========================================================
# Merge Data
# ==========================================================


def merge_data():

    clusters = load_cluster_labels()

    financials = load_financial_data()

    merged = financials.merge(clusters, on="company_id", how="left")

    return merged


# ==========================================================
# Cluster Summary Statistics
# ==========================================================


def generate_cluster_summary(df):

    summary = df.groupby(["cluster_id", "cluster_name"], as_index=False).agg(
        companies=("company_id", "count"),
        average_roe=("return_on_equity_pct", "mean"),
        average_debt=("debt_to_equity", "mean"),
        average_revenue_cagr=("revenue_cagr_5yr", "mean"),
        average_fcf=("free_cash_flow_cr", "mean"),
        average_opm=("operating_profit_margin_pct", "mean"),
    )

    summary = summary.round(2)

    return summary


# ==========================================================
# Sector Distribution
# ==========================================================


def generate_sector_distribution(df):

    sector_distribution = (
        df.groupby(["cluster_name", "broad_sector"], as_index=False)
        .agg(companies=("company_id", "count"))
        .sort_values(["cluster_name", "companies"], ascending=[True, False])
    )

    return sector_distribution


# ==========================================================
# Top Companies in Each Cluster
# ==========================================================


def generate_top_companies(df):

    ranking = df.sort_values(
        ["cluster_name", "return_on_equity_pct"], ascending=[True, False]
    )

    top_companies = ranking.groupby("cluster_name").head(5)[
        [
            "cluster_name",
            "company_id",
            "company_name",
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
        ]
    ]

    top_companies = top_companies.round(2)

    return top_companies


# ==========================================================
# Save Reports
# ==========================================================


def save_reports(summary, sector_distribution, top_companies):

    summary_file = OUTPUT_DIR / "cluster_summary.csv"

    sector_file = OUTPUT_DIR / "cluster_sector_distribution.csv"

    top_file = OUTPUT_DIR / "cluster_top_companies.csv"

    summary.to_csv(summary_file, index=False)

    sector_distribution.to_csv(sector_file, index=False)

    top_companies.to_csv(top_file, index=False)

    return summary_file, sector_file, top_file


# ==========================================================
# Validation
# ==========================================================


def validate(summary, sector_distribution, top_companies):

    print("\n" + "=" * 60)
    print("Cluster Profiling Validation")
    print("=" * 60)

    print(f"Clusters Found        : {summary.shape[0]}")
    print(f"Sector Records        : {sector_distribution.shape[0]}")
    print(f"Top Company Records   : {top_companies.shape[0]}")

    print("\nCluster Summary\n")

    print(summary[["cluster_name", "companies", "average_roe"]])

    if summary.shape[0] == 5:
        print("\nPASS : All 5 clusters profiled.")

    else:
        print("\nWARNING : Expected 5 clusters.")


# ==========================================================
# Main
# ==========================================================


def main():

    print("\nLoading clustered dataset...")

    df = merge_data()

    print(f"Companies Loaded : {len(df)}")

    print("\nGenerating cluster summary...")

    summary = generate_cluster_summary(df)

    print("Generating sector distribution...")

    sector_distribution = generate_sector_distribution(df)

    print("Generating top company list...")

    top_companies = generate_top_companies(df)

    print("Saving reports...")

    summary_file, sector_file, top_file = save_reports(
        summary, sector_distribution, top_companies
    )

    validate(summary, sector_distribution, top_companies)

    print("\nGenerated Files")

    print(summary_file)

    print(sector_file)

    print(top_file)

    print("\nSprint 6 - Day 37 Completed Successfully")


if __name__ == "__main__":
    main()
