import sqlite3

conn = sqlite3.connect("db/nifty100.db")

conn.execute(
    "PRAGMA foreign_keys = ON"
)

rows = conn.execute(
    "PRAGMA foreign_key_check"
).fetchall()

print(rows)

conn.close()