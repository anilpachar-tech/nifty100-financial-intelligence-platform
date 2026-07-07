"""
Sprint 3 - Day 15

Financial Screener Engine
"""

import sqlite3
import pandas as pd
import yaml

DB_PATH = "db/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"


def load_data():

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    sectors = pd.read_sql(
        "SELECT company_id, broad_sector FROM sectors",
        conn
    )

    conn.close()

    return ratios, sectors


def load_config():

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)

def prepare_master_dataset():

    ratios, sectors = load_data()

    master = ratios.merge(
        sectors,
        on="company_id",
        how="left"
    )

    master = (
    master
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .tail(1)
    )

    master = master.reset_index(drop=True)

    return master

def apply_filters(
    df: pd.DataFrame,
    filters: dict
) -> pd.DataFrame:

    result = df.copy()

    # ROE Filter
    if "roe_min" in filters:
        result = result[
            result["return_on_equity_pct"] >=
            filters["roe_min"]
        ]

    # Debt to Equity Filter
    if "debt_to_equity_max" in filters:

        financial_mask = (
            result["broad_sector"]
            .str.lower()
            == "financials"
        )

        non_financial = result[
            ~financial_mask
        ]

        financial = result[
            financial_mask
        ]

        non_financial = non_financial[
            non_financial["debt_to_equity"] <=
            filters["debt_to_equity_max"]
        ]

        result = pd.concat(
            [financial, non_financial],
            ignore_index=True
        )

    # Free Cash Flow
    if "free_cash_flow_min" in filters:
        result = result[
            result["free_cash_flow_cr"] >=
            filters["free_cash_flow_min"]
        ]

    # Revenue CAGR
    if "revenue_cagr_5yr_min" in filters:
        result = result[
            result["revenue_cagr_5yr"] >=
            filters["revenue_cagr_5yr_min"]
        ]

    # PAT CAGR
    if "pat_cagr_5yr_min" in filters:
        result = result[
            result["pat_cagr_5yr"] >=
            filters["pat_cagr_5yr_min"]
        ]

    return result

if __name__ == "__main__":

   master = prepare_master_dataset()

config = load_config()

print("=" * 60)
print("Master Dataset")
print("=" * 60)

print("Rows :", len(master))
print()

print(master[
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "broad_sector"
    ]
].head())

print()
print("=" * 60)
print("Configuration Loaded")
print("=" * 60)

print(config.keys())

print()
print("=" * 60)
print("Quality Compounder Screener")
print("=" * 60)

quality = apply_filters(
    master,
    config["quality_compounder"]
)

print("Companies Found :", len(quality))
print()

print(
    quality[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr"
        ]
    ].head(20)
)