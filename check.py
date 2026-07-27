import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT COUNT(*) AS companies
FROM companies
"""

print(pd.read_sql(query, conn))

query = """
SELECT COUNT(DISTINCT company_id) AS ratios
FROM financial_ratios
"""

print(pd.read_sql(query, conn))

conn.close()