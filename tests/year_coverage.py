import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

companies = [
    "PFC",
    "VEDL",
    "IOC",
    "BRITANNIA",
    "EICHERMOT"
]

summary = []

for company in companies:

    query = f"""
    SELECT DISTINCT year
    FROM balancesheet
    WHERE company_id = '{company}'
    """

    df = pd.read_sql(query, conn)

    years = len(df)

    summary.append(
        {
            "company": company,
            "years_available": years
        }
    )

summary_df = pd.DataFrame(summary)

print("\n===== YEAR COVERAGE SUMMARY =====\n")
print(summary_df)

conn.close()