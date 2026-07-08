import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cur = conn.cursor()

columns = [
    ("pe", "REAL"),
    ("pb", "REAL"),
    ("dividend_yield", "REAL")
]

for name, dtype in columns:
    try:
        cur.execute(f"ALTER TABLE financial_ratios ADD COLUMN {name} {dtype}")
        print(f"{name} added")
    except Exception as e:
        print(e)

conn.commit()

print("\nUpdated Schema:\n")

cur.execute("PRAGMA table_info(financial_ratios)")

for row in cur.fetchall():
    print(row)

conn.close()