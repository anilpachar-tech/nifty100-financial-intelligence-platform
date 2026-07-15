import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT *
FROM prosandcons
WHERE company_id='ABB'
""", conn)

print(df)

conn.close()