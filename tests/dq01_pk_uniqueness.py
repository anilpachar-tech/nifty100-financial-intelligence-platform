import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "market_cap",
    "financial_ratios",
    "peer_groups"
]

print("\n===== DQ-01 PK UNIQUENESS =====\n")

for table in tables:

    query = f"""
    SELECT COUNT(*) - COUNT(DISTINCT id)
    FROM {table}
    """

    duplicates = conn.execute(query).fetchone()[0]

    print(f"{table} : {duplicates}")

conn.close()