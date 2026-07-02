"""
Sprint 2 - Day 11

Generate Capital Allocation Report
"""

import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import (
    capital_allocation_pattern
)

DB_PATH = "db/nifty100.db"
OUTPUT_FILE = "output/capital_allocation.csv"


def main():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cashflow
    """

    df = pd.read_sql(query, conn)

    conn.close()

    output = []

    for _, row in df.iterrows():

        cfo = row["operating_activity"]
        cfi = row["investing_activity"]
        cff = row["financing_activity"]

        output.append(
            {
                "company_id": row["company_id"],
                "year": row["year"],
                "cfo_sign": "+" if cfo >= 0 else "-",
                "cfi_sign": "+" if cfi >= 0 else "-",
                "cff_sign": "+" if cff >= 0 else "-",
                "pattern_label":
                    capital_allocation_pattern(
                        cfo,
                        cfi,
                        cff
                    )
            }
        )

    result = pd.DataFrame(output)

    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 50)
    print("Capital Allocation Report Generated")
    print("=" * 50)
    print(result.head())


if __name__ == "__main__":
    main()