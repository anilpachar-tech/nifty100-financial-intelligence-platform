import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT
    company_id,
    year,
    pe,
    pb,
    dividend_yield
FROM financial_ratios
WHERE pe IS NOT NULL
LIMIT 10
""", conn)

print(df)

conn.close()