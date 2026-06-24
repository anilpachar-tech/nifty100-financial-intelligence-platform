import pandas as pd
import sqlite3

DB_PATH = "db/nifty100.db"

files = [
    ("data/raw/companies.xlsx", "companies", 1),
    ("data/raw/profitandloss.xlsx", "profitandloss", 1),
    ("data/raw/balancesheet.xlsx", "balancesheet", 1),
    ("data/raw/cashflow.xlsx", "cashflow", 1),
    ("data/raw/analysis.xlsx", "analysis", 1),
    ("data/raw/documents.xlsx", "documents", 1),
    ("data/raw/prosandcons.xlsx", "prosandcons", 1),

    ("data/raw/supporting datasets/sectors.xlsx", "sectors", 0),
    ("data/raw/supporting datasets/stock_prices.xlsx", "stock_prices", 0),
    ("data/raw/supporting datasets/market_cap.xlsx", "market_cap", 0),
    ("data/raw/supporting datasets/financial_ratios.xlsx", "financial_ratios", 0),
    ("data/raw/supporting datasets/peer_groups.xlsx", "peer_groups", 0)
]

audit = []

conn = sqlite3.connect(DB_PATH)

for file_path, table_name, header_row in files:

    try:

        print(f"\nLoading -> {table_name}")

        df = pd.read_excel(
            file_path,
            header=header_row
        )

        # Day 6 Data Quality Fix
        if table_name in [
            "profitandloss",
            "balancesheet",
            "cashflow",
            "financial_ratios"
        ]:

            before_rows = len(df)

            df = df.drop_duplicates(
                subset=["company_id", "year"]
            )

            removed = before_rows - len(df)

            print(
                f"Removed {removed} duplicate rows from {table_name}"
            )

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

        audit.append(
            {
                "table": table_name,
                "rows_loaded": len(df),
                "status": "SUCCESS"
            }
        )

        print(f"Loaded {table_name} : {len(df)} rows")

    except Exception as e:

        audit.append(
            {
                "table": table_name,
                "rows_loaded": 0,
                "status": f"FAILED : {e}"
            }
        )

        print("\n==============================")
        print(f"ERROR IN TABLE : {table_name}")
        print(f"FILE : {file_path}")
        print(f"ERROR : {e}")
        print("==============================")

        break

conn.commit()
conn.close()

audit_df = pd.DataFrame(audit)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print("\nLoad Audit Generated")
print("Data Quality Cleaning Applied Successfully")