import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT *
FROM peer_percentiles
LIMIT 10
""", conn)

print(df)

conn.close()