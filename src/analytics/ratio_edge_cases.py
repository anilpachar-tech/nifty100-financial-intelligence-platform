"""
Sprint 2 - Day 13

Bank ROCE Carve-Out
Edge Case Detection
"""

import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("Reading Tables")
print("=" * 60)

companies = pd.read_sql(
    "SELECT company_name, roce_percentage, roe_percentage FROM companies",
    conn
)

sectors = pd.read_sql(
    "SELECT company_id, broad_sector FROM sectors",
    conn
)

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity
    FROM financial_ratios
    """,
    conn
)

print("Companies :", len(companies))
print("Sectors :", len(sectors))
print("Financial Ratios :", len(ratios))

print()
print("=" * 60)
print("Identifying Financial Companies")
print("=" * 60)

financial_companies = sectors[
    sectors["broad_sector"].str.strip().str.lower() == "financials"
]

print("Financial Companies :", len(financial_companies))
print()

print(financial_companies[
    ["company_id", "broad_sector"]
])

print()
print("=" * 60)
print("Applying D/E Carve-Out")
print("=" * 60)

financial_ids = set(financial_companies["company_id"])

ratios["high_leverage_warning"] = (
    (ratios["debt_to_equity"] > 5) &
    (~ratios["company_id"].isin(financial_ids))
)

print(
    "High Leverage Warnings :",
    ratios["high_leverage_warning"].sum()
)

print()

print(
    ratios[
        ratios["high_leverage_warning"]
    ][
        [
            "company_id",
            "year",
            "debt_to_equity"
        ]
    ].head(10)
)

print()
print("=" * 60)
print("ROCE & ROE Cross Check")
print("=" * 60)

comparison = pd.read_sql(
    """
    SELECT
        fr.company_id,
        fr.year,
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        c.roe_percentage,
        c.roce_percentage
    FROM financial_ratios fr
    JOIN companies c
        ON fr.company_id = c.id
    """,
    conn
)

comparison["roe_difference"] = (
    comparison["return_on_equity_pct"] -
    comparison["roe_percentage"]
).abs()

comparison["roce_difference"] = (
    comparison["return_on_capital_employed_pct"] -
    comparison["roce_percentage"]
).abs()

edge_cases = comparison[
    (comparison["roe_difference"] > 5) |
    (comparison["roce_difference"] > 5)
].copy()

print("Edge Cases :", len(edge_cases))
print()

print(edge_cases.head(10))

def classify(row):

    if row["roe_difference"] > 20:
        return "Data Source Issue"

    if row["roce_difference"] > 20:
        return "Data Source Issue"

    if (
        row["roe_difference"] > 5 and
        row["roce_difference"] > 5
    ):
        return "Formula Discrepancy"

    return "Version Difference"


edge_cases["category"] = edge_cases.apply(
    classify,
    axis=1
)

print()
print(edge_cases[
    [
        "company_id",
        "year",
        "roe_difference",
        "roce_difference",
        "category"
    ]
].head(10))

import os

os.makedirs("output", exist_ok=True)

edge_cases.to_csv(
    "output/ratio_edge_cases.log",
    index=False
)

print()
print("=" * 60)
print("Edge Case Log Generated")
print("=" * 60)
print("output/ratio_edge_cases.log")