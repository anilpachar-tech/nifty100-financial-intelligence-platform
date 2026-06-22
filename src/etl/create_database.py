import sqlite3
from pathlib import Path

db_path = "db/nifty100.db"
schema_path = "db/schema.sql"

conn = sqlite3.connect(db_path)

with open(schema_path, "r", encoding="utf-8") as file:
    schema = file.read()

conn.executescript(schema)

conn.commit()
conn.close()

print("Database Created Successfully")
print("Database :", db_path)