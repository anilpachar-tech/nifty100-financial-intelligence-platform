import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios"
]

for table in tables:

    query = f"""
    SELECT COUNT(*) AS duplicate_rows
    FROM (
        SELECT company_id, year
        FROM {table}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
    )
    """

    duplicates = pd.read_sql(query, conn)

    print(f"\n{table}")
    print(duplicates)

conn.close()