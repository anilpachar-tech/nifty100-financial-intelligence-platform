import logging
import sqlite3
from pathlib import Path

import pandas as pd

# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

CAPITAL_FILE = OUTPUT_DIR / "capital_allocation.csv"

CASHFLOW_FILE = OUTPUT_DIR / "cashflow_intelligence.xlsx"

PATTERN_FILE = OUTPUT_DIR / "pattern_changes.csv"

LOG_FILE = OUTPUT_DIR / "capital_allocation_report.log"


OUTPUT_DIR.mkdir(exist_ok=True)


# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# =====================================================
# Database
# =====================================================


def connect_database():

    logger.info("Connecting database...")

    return sqlite3.connect(DB_FILE)


# =====================================================
# Load Companies
# =====================================================


def load_companies(conn):

    query = """

    SELECT

        id AS company_id,

        company_name

    FROM companies

    ORDER BY id

    """

    companies = pd.read_sql(query, conn)

    companies["company_id"] = (
        companies["company_id"].astype(str).str.strip().str.upper()
    )

    logger.info("Companies Loaded : %d", len(companies))

    return companies


# =====================================================
# Load Capital Allocation
# =====================================================


def load_capital_allocation():

    capital = pd.read_csv(CAPITAL_FILE)

    capital["company_id"] = capital["company_id"].astype(str).str.strip().str.upper()

    # Historical ticker mapping

    ticker_map = {"AGTL": "ATGL", "MCDOWELL-N": "UNITDSPR", "MOTHERSUMI": "MSUMI"}

    capital["company_id"] = capital["company_id"].replace(ticker_map)

    logger.info("Capital Allocation Rows : %d", len(capital))

    return capital


# =====================================================
# Load Cashflow Intelligence
# =====================================================


def load_cashflow_intelligence():

    cashflow = pd.read_excel(CASHFLOW_FILE)

    cashflow["company_id"] = cashflow["company_id"].astype(str).str.strip().str.upper()

    logger.info("Cashflow Intelligence Rows : %d", len(cashflow))

    return cashflow


# =====================================================
# Verification
# =====================================================


def verify_capital_allocation(companies_df, capital_df):

    logger.info("Running Verification...")

    expected_ids = set(companies_df["company_id"])

    actual_ids = set(capital_df["company_id"])

    extra_ids = sorted(actual_ids - expected_ids)

    missing_ids = sorted(expected_ids - actual_ids)

    valid_df = capital_df[capital_df["company_id"].isin(expected_ids)].copy()

    years = valid_df.groupby("company_id").size()

    low_history = []

    for company_id, total_years in years.items():

        if total_years < 5:

            low_history.append((company_id, int(total_years)))

    verification = {
        "expected_companies": len(expected_ids),
        "found_companies": len(expected_ids & actual_ids),
        "extra_companies": len(extra_ids),
        "missing_companies": len(missing_ids),
        "extra_ids": extra_ids,
        "missing_ids": missing_ids,
        "minimum_years": int(years.min()),
        "maximum_years": int(years.max()),
        "average_years": round(years.mean(), 2),
        "low_history": low_history,
    }

    logger.info(verification)

    return (verification, valid_df)


# =====================================================
# Year Utilities
# =====================================================


def prepare_years(capital_df):

    df = capital_df.copy()

    df["year_num"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .astype(int)
        .apply(lambda x: 2000 + x if x < 50 else 1900 + x)
    )

    return df


# =====================================================
# Latest Year Distribution
# =====================================================


def generate_distribution_summary(capital_df):

    logger.info("Generating Distribution Summary...")

    df = prepare_years(capital_df)

    latest_year = df["year_num"].max()

    latest_df = df[df["year_num"] == latest_year].copy()

    distribution = (
        latest_df.groupby("pattern_label")
        .agg(companies=("company_id", "nunique"))
        .reset_index()
        .sort_values("companies", ascending=False)
    )

    distribution.insert(0, "year", latest_df.iloc[0]["year"])

    logger.info("Distribution Generated.")

    return (latest_df, distribution)


# =====================================================
# Update Cashflow Intelligence
# =====================================================


def update_cashflow_intelligence(cashflow_df, latest_df):

    logger.info("Updating Cashflow Intelligence...")

    latest_pattern = latest_df[["company_id", "pattern_label"]].drop_duplicates(
        subset="company_id"
    )

    updated = cashflow_df.merge(latest_pattern, on="company_id", how="left")

    updated.rename(
        columns={"pattern_label": "capital_allocation_pattern"}, inplace=True
    )

    logger.info("Cashflow Updated.")

    return updated


# =====================================================
# Pattern Changes
# =====================================================


def generate_pattern_changes(capital_df):

    logger.info("Generating Pattern Changes...")

    df = prepare_years(capital_df)

    df = df.sort_values(["company_id", "year_num"])

    changes = []

    for company_id, group in df.groupby("company_id"):

        group = group.reset_index(drop=True)

        for i in range(1, len(group)):

            previous = group.loc[i - 1, "pattern_label"]

            current = group.loc[i, "pattern_label"]

            if previous == current:
                continue

            changes.append(
                {
                    "company_id": company_id,
                    "from_year": group.loc[i - 1, "year"],
                    "to_year": group.loc[i, "year"],
                    "previous_pattern": previous,
                    "current_pattern": current,
                }
            )

    changes_df = pd.DataFrame(changes)

    logger.info("Pattern Changes : %d", len(changes_df))

    return changes_df


# =====================================================
# Save Outputs
# =====================================================


def save_reports(updated_df, changes_df):

    updated_df.to_excel(CASHFLOW_FILE, index=False)

    changes_df.to_csv(PATTERN_FILE, index=False)

    logger.info("Reports Saved.")


# =====================================================
# Console Output
# =====================================================


def print_distribution_summary(distribution_df):

    print("\n" + "=" * 60)
    print("Capital Allocation Distribution")
    print("=" * 60)

    print(distribution_df.to_string(index=False))

    print("=" * 60)


# =====================================================
# Summary
# =====================================================


def print_summary(verification, distribution_df, pattern_changes_df):

    print("\n" + "=" * 60)
    print("Sprint 5 - Day 32")
    print("Capital Allocation Report")
    print("=" * 60)

    print(f"Expected Companies : {verification['expected_companies']}")

    print(f"Companies Found    : {verification['found_companies']}")

    print(f"Missing Companies  : {verification['missing_companies']}")

    print(f"Minimum Years      : {verification['minimum_years']}")

    print(f"Maximum Years      : {verification['maximum_years']}")

    print(f"Average Years      : {verification['average_years']}")

    low_history = verification.get("low_history", [])

    print(f"Companies <5 Years : {len(low_history)}")

    if low_history:

        print("\nCompanies having less than 5 years history")
        print("-" * 60)

        for cid, yrs in low_history:
            print(f"{cid:<15} {yrs} years")

    print("\nPattern Summary")
    print("-" * 60)

    print(f"Pattern Categories : {len(distribution_df)}")

    print(f"Pattern Changes    : {len(pattern_changes_df)}")

    if verification["extra_ids"]:

        print("\nAdditional IDs Found (Ignored)")
        print("-" * 60)

        for cid in verification["extra_ids"]:
            print(f" - {cid}")

    if verification["missing_ids"]:

        print("\nMissing IDs")

        for cid in verification["missing_ids"]:
            print(f" - {cid}")

    print("\nGenerated Files")
    print("-" * 60)

    print(CASHFLOW_FILE)
    print(PATTERN_FILE)
    print(LOG_FILE)

    print("=" * 60)


# =====================================================
# Main
# =====================================================


def main():

    logger.info("=" * 60)
    logger.info("Sprint 5 Day 32 Started")

    conn = None

    try:

        conn = connect_database()

        companies_df = load_companies(conn)

        capital_df = load_capital_allocation()

        cashflow_df = load_cashflow_intelligence()

        verification, capital_df = verify_capital_allocation(companies_df, capital_df)

        latest_df, distribution_df = generate_distribution_summary(capital_df)

        updated_df = update_cashflow_intelligence(cashflow_df, latest_df)

        pattern_changes_df = generate_pattern_changes(capital_df)

        save_reports(updated_df, pattern_changes_df)

        print_distribution_summary(distribution_df)

        print_summary(verification, distribution_df, pattern_changes_df)

        logger.info("Sprint 5 Day 32 Completed Successfully.")

    except Exception as e:

        logger.exception(e)

        print("\nERROR")
        print("-" * 60)
        print(e)
        print("-" * 60)

    finally:

        if conn is not None:
            conn.close()


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    main()
