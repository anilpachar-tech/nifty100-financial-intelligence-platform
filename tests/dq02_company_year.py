import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap"
]

print("\n===== DQ-02 COMPANY_ID + YEAR UNIQUENESS =====\n")

for table in tables:

    query = f"""
    SELECT COUNT(*)
    FROM (
        SELECT company_id, year, COUNT(*) as cnt
        FROM {table}
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
    )
    """

    duplicates = conn.execute(query).fetchone()[0]

    print(f"{table} : {duplicates}")

conn.close()