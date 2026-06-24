import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

table = "balancesheet"

query = f"""
SELECT
    company_id,
    year,
    COUNT(*) as duplicate_count
FROM {table}
GROUP BY company_id, year
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC
"""

df = pd.read_sql(query, conn)

print(df.head(20))

conn.close()