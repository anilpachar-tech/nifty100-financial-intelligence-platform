import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cur = conn.cursor()

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

print("\n===== ROW COUNT VERIFICATION =====\n")

for table in tables:

    cur.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cur.fetchone()[0]

    print(f"{table} : {count}")

conn.close()