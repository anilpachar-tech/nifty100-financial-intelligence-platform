import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("SELECT * FROM stock_prices LIMIT 5", conn)

print("Columns:")
print(df.columns.tolist())

print("\nData:")
print(df)

conn.close()