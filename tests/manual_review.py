import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT DISTINCT company_id
FROM balancesheet
ORDER BY RANDOM()
LIMIT 5
"""

companies = pd.read_sql(query, conn)

print("\n===== RANDOM 5 COMPANIES =====\n")
print(companies)

conn.close()