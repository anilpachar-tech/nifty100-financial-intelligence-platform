"""
Sprint 2 - Day 12

Populate financial_ratios table
"""

import sqlite3
import pandas as pd

from src.analytics.ratios import *

from src.analytics.cagr import *

from src.analytics.cashflow_kpis import *

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("Reading Database Tables")
print("=" * 60)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print()

print("Companies :", len(companies))
print("Profit & Loss :", len(profit))
print("Balance Sheet :", len(balance))
print("Cashflow :", len(cashflow))
print("Financial Ratios :", len(financial))

print()
print("=" * 60)
print("Preparing Master Dataset")
print("=" * 60)

master = (
    profit
    .merge(
        balance,
        on=["company_id", "year"],
        how="inner",
        suffixes=("_pl", "_bs")
    )
    .merge(
        cashflow,
        on=["company_id", "year"],
        how="inner"
    )
)

print("Merged Records :", len(master))
print()
print(master[["company_id", "year"]].head())

print()
print("=" * 60)
print("Calculating KPIs")
print("=" * 60)

results = []

for _, row in master.iterrows():

    try:

        npm = net_profit_margin(
            row["net_profit"],
            row["sales"]
        )

        opm = operating_profit_margin(
            row["operating_profit"],
            row["sales"]
        )

        roe = return_on_equity(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"]
        )

        de = debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"]
        )

        icr = interest_coverage_ratio(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        )

        turnover = asset_turnover(
            row["sales"],
            row["total_assets"]
        )

        fcf = free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        )

        capex, capex_label = capex_intensity(
            row["investing_activity"],
            row["sales"]
        )

        # Earnings Per Share
        eps = row["eps"]

        # Book Value Per Share
        if row["equity_capital"] != 0:
            book_value = round(
                (
                    row["equity_capital"] +
                    row["reserves"]
                ) /
                row["equity_capital"],
                2
            )
        else:
            book_value = None

        # Dividend Payout Ratio
        dividend = row["dividend_payout"]

        # Total Debt
        total_debt = row["borrowings"]

        # Cash From Operations
        cfo = row["operating_activity"]

        # Composite Quality Score
        score = 0

        if roe is not None and roe > 15:
            score += 1

        if de is not None and de < 1:
            score += 1

        if icr is not None and icr > 3:
            score += 1

        if turnover is not None and turnover > 1:
            score += 1

        if npm is not None and npm > 10:
            score += 1

        composite_score = score


        results.append(
            {
                "company_id": row["company_id"],
                "year": row["year"],

                "net_profit_margin_pct": npm,
                "operating_profit_margin_pct": opm,
                "return_on_equity_pct": roe,
                "debt_to_equity": de,
                "interest_coverage": icr,
                "asset_turnover": turnover,

                "free_cash_flow_cr": fcf,
                "capex_cr": capex,

                "earnings_per_share": eps,
                "book_value_per_share": book_value,
                "dividend_payout_ratio_pct": dividend,

                "total_debt_cr": total_debt,
                "cash_from_operations_cr": cfo,

                "composite_quality_score": composite_score
            }
        )        

    except Exception as e:

        print(
            f"Error : {row['company_id']} "
            f"{row['year']} -> {e}"
        )

result_df = pd.DataFrame(results)

print()
print("Calculated Rows :", len(result_df))
print()

print(result_df.head())

print()
print("=" * 60)
print("Calculating 5-Year CAGR")
print("=" * 60)

# Default columns
result_df["revenue_cagr_5yr"] = None
result_df["pat_cagr_5yr"] = None
result_df["eps_cagr_5yr"] = None

for company in result_df["company_id"].unique():

    company_data = (
        master[master["company_id"] == company]
        .copy()
    )

    company_data = company_data.sort_values("year")

    if len(company_data) < 6:
        continue

    start = company_data.iloc[-6]
    end = company_data.iloc[-1]

    revenue, _ = revenue_cagr(
        start["sales"],
        end["sales"],
        5
    )

    pat, _ = pat_cagr(
        start["net_profit"],
        end["net_profit"],
        5
    )

    eps, _ = eps_cagr(
        start["eps"],
        end["eps"],
        5
    )

    result_df.loc[
        result_df["company_id"] == company,
        "revenue_cagr_5yr"
    ] = revenue

    result_df.loc[
        result_df["company_id"] == company,
        "pat_cagr_5yr"
    ] = pat

    result_df.loc[
        result_df["company_id"] == company,
        "eps_cagr_5yr"
    ] = eps

    print()
print(result_df[
    [
        "company_id",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr"
    ]
].head())

print()
print("=" * 60)
print("Matching financial_ratios IDs")
print("=" * 60)

financial_keys = financial[
    ["id", "company_id", "year"]
]

result_df = result_df.merge(
    financial_keys,
    on=["company_id", "year"],
    how="left"
)

print("Matched IDs :", result_df["id"].notna().sum())

print()
print("=" * 60)
print("Updating financial_ratios Table")
print("=" * 60)

cursor = conn.cursor()

for _, row in result_df.iterrows():

    cursor.execute(
        """
        UPDATE financial_ratios
        SET
            net_profit_margin_pct=?,
            operating_profit_margin_pct=?,
            return_on_equity_pct=?,
            debt_to_equity=?,
            interest_coverage=?,
            asset_turnover=?,
            free_cash_flow_cr=?,
            capex_cr=?,
            earnings_per_share=?,
            book_value_per_share=?,
            dividend_payout_ratio_pct=?,
            total_debt_cr=?,
            cash_from_operations_cr=?,
            revenue_cagr_5yr=?,
            pat_cagr_5yr=?,
            eps_cagr_5yr=?,
            composite_quality_score=?
        WHERE id=?
        """,
        (
            row["net_profit_margin_pct"],
            row["operating_profit_margin_pct"],
            row["return_on_equity_pct"],
            row["debt_to_equity"],
            row["interest_coverage"],
            row["asset_turnover"],
            row["free_cash_flow_cr"],
            row["capex_cr"],
            row["earnings_per_share"],
            row["book_value_per_share"],
            row["dividend_payout_ratio_pct"],
            row["total_debt_cr"],
            row["cash_from_operations_cr"],
            row["revenue_cagr_5yr"],
            row["pat_cagr_5yr"],
            row["eps_cagr_5yr"],
            row["composite_quality_score"],
            row["id"]
        )
    )

conn.commit()

print("Database Updated Successfully")

print()
print("=" * 60)
print("Verifying financial_ratios Table")
print("=" * 60)

count = pd.read_sql(
    """
    SELECT COUNT(*) AS total_rows
    FROM financial_ratios
    """,
    conn
)

print(count)

spot = pd.read_sql("""
SELECT
    company_id,
    year,
    return_on_equity_pct,
    revenue_cagr_5yr
FROM financial_ratios
WHERE company_id IN ('ABB','TCS','INFY')
ORDER BY company_id, year
LIMIT 15
""", conn)

print()
print("=" * 60)
print("3 Company Spot Check")
print("=" * 60)
print(spot)

conn.close()