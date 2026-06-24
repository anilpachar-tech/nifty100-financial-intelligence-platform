import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT *
FROM balancesheet
WHERE company_id='PNB'
AND year='Mar 2013'
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()