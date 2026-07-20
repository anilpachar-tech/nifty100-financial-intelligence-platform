import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    company_id,
    COUNT(*) AS years_available
FROM financial_ratios
GROUP BY company_id
HAVING COUNT(*) < 10
ORDER BY years_available, company_id;
"""

df = pd.read_sql(query, conn)

conn.close()

print(df)

print("\nTotal Companies with Partial Data:", len(df))