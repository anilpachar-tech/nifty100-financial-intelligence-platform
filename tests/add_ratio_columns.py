import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

columns = [

    "ALTER TABLE financial_ratios ADD COLUMN revenue_cagr_5yr REAL",

    "ALTER TABLE financial_ratios ADD COLUMN pat_cagr_5yr REAL",

    "ALTER TABLE financial_ratios ADD COLUMN eps_cagr_5yr REAL",

    "ALTER TABLE financial_ratios ADD COLUMN composite_quality_score REAL"

]

for query in columns:

    try:

        cursor.execute(query)

        print("Added:", query)

    except Exception:

        print("Already Exists")

conn.commit()

conn.close()

print("\nColumns Ready")