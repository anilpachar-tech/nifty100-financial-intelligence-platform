"""
Sprint 3 - Day 18

Peer Percentile Rankings
"""

import pandas as pd
import sqlite3

DB_PATH = "db/nifty100.db"


def load_data():

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    peers = pd.read_sql(
        "SELECT * FROM peer_groups",
        conn
    )

    conn.close()

    return ratios, peers

def prepare_master():

    ratios, peers = load_data()

    master = ratios.merge(
        peers[
            [
                "company_id",
                "peer_group_name"
            ]
        ],
        on="company_id",
        how="left"
    )

    missing = master["peer_group_name"].isna().sum()
    
    if missing > 0:
        print()
        print(f"No peer group assigned : {missing} records")

    return master

def calculate_percentile(master):

    metrics = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "eps_cagr_5yr",
        "interest_coverage",
        "asset_turnover"
    ]

    results = []

    grouped = master.groupby("peer_group_name")

    for group_name, group in grouped:

        if pd.isna(group_name):
            continue

        for metric in metrics:

            temp = group.copy()

            if metric == "debt_to_equity":

                temp["percentile_rank"] = (
                    1 - temp[metric].rank(pct=True)
                ) * 100

            else:

                temp["percentile_rank"] = (
                    temp[metric].rank(pct=True)
                ) * 100

            for _, row in temp.iterrows():

                results.append({
                    "company_id": row["company_id"],
                    "peer_group_name": group_name,
                    "metric": metric,
                    "value": row[metric],
                    "percentile_rank": round(
                        row["percentile_rank"],
                        2
                    ),
                    "year": row["year"]
                })

    return pd.DataFrame(results)

if __name__ == "__main__":

    master = prepare_master()

    print("=" * 60)
    print("Peer Master Dataset")
    print("=" * 60)

    print("Rows :", len(master))
    print()

    print(master.head())

peer_percentiles = calculate_percentile(master)

print()
print("=" * 60)
print("Peer Percentiles")
print("=" * 60)

print("Rows :", len(peer_percentiles))
print()

print(peer_percentiles.head(20))

print()
print("=" * 60)
print("Saving Peer Percentiles")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)

# Purana data remove
conn.execute("DELETE FROM peer_percentiles")

peer_percentiles.to_sql(
    "peer_percentiles",
    conn,
    if_exists="append",
    index=False
)

count = pd.read_sql(
    """
    SELECT COUNT(*) AS total_rows
    FROM peer_percentiles
    """,
    conn
)

print(count)

conn.close()

print()
print("Peer Percentiles Saved Successfully")
