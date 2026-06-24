import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "financial_ratios"
]

for table in tables:

    query = f"""
    SELECT DISTINCT company_id
    FROM {table}
    WHERE company_id NOT IN (
        SELECT id
        FROM companies
    )
    ORDER BY company_id
    """

    df = pd.read_sql(query, conn)

    print(f"\n===== {table} =====")
    print(df)

conn.close()