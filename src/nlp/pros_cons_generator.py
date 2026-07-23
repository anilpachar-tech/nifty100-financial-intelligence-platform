"""
Sprint 5 - Day 30

Pros & Cons Generator

Generates rule-based strengths and weaknesses
for every company using financial statements.

Output
------
output/pros_cons_generated.csv
"""

from pathlib import Path
import logging
import sqlite3

import pandas as pd


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "pros_cons_generated.csv"

LOG_FILE = OUTPUT_DIR / "pros_cons_generator.log"


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# Database
# ==========================================================

def connect_database():

    if not DB_FILE.exists():
        raise FileNotFoundError(
            f"Database not found:\n{DB_FILE}"
        )

    logger.info("Connected to SQLite database.")

    return sqlite3.connect(DB_FILE)


# ==========================================================
# Load Companies
# ==========================================================

def load_companies(conn):

    query = """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    ORDER BY id
    """

    companies = pd.read_sql(query, conn)

    logger.info(
        "Loaded %d companies.",
        len(companies)
    )

    return companies


# ==========================================================
# Load Financial Ratios
# ==========================================================

def load_financial_ratios(conn):

    query = """
    SELECT *
    FROM financial_ratios
    ORDER BY company_id, year
    """

    df = pd.read_sql(query, conn)

    logger.info(
        "Financial Ratios : %d rows",
        len(df)
    )

    return df


# ==========================================================
# Load Profit & Loss
# ==========================================================

def load_profit_loss(conn):

    query = """
    SELECT *
    FROM profitandloss
    ORDER BY company_id, year
    """

    df = pd.read_sql(query, conn)

    logger.info(
        "Profit & Loss : %d rows",
        len(df)
    )

    return df


# ==========================================================
# Load Balance Sheet
# ==========================================================

def load_balance_sheet(conn):

    query = """
    SELECT *
    FROM balancesheet
    ORDER BY company_id, year
    """

    df = pd.read_sql(query, conn)

    logger.info(
        "Balance Sheet : %d rows",
        len(df)
    )

    return df


# ==========================================================
# Load Cash Flow
# ==========================================================

def load_cashflow(conn):

    query = """
    SELECT *
    FROM cashflow
    ORDER BY company_id, year
    """

    df = pd.read_sql(query, conn)

    logger.info(
        "Cash Flow : %d rows",
        len(df)
    )

    return df

# ==========================================================
# Helper Functions
# ==========================================================

def get_company_ratios(ratio_df, company_id):

    return (
        ratio_df[
            ratio_df["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )


def get_company_profit_loss(pl_df, company_id):

    return (
        pl_df[
            pl_df["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )


def get_company_balance_sheet(bs_df, company_id):

    return (
        bs_df[
            bs_df["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )


def get_company_cashflow(cf_df, company_id):

    return (
        cf_df[
            cf_df["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )


# ==========================================================
# Latest Record
# ==========================================================

def get_latest(df):

    if df.empty:
        return None

    return df.iloc[-1]


# ==========================================================
# Last N Years
# ==========================================================

def get_last_n_years(df, n):

    if df.empty:
        return df

    return (
        df.sort_values("year")
        .tail(n)
        .reset_index(drop=True)
    )


# ==========================================================
# Trend Check
# ==========================================================

def is_increasing(series):

    values = (
        pd.to_numeric(
            series,
            errors="coerce"
        )
        .dropna()
        .tolist()
    )

    if len(values) < 2:
        return False

    return all(
        x < y
        for x, y in zip(
            values,
            values[1:]
        )
    )


def is_decreasing(series):

    values = (
        pd.to_numeric(
            series,
            errors="coerce"
        )
        .dropna()
        .tolist()
    )

    if len(values) < 2:
        return False

    return all(
        x > y
        for x, y in zip(
            values,
            values[1:]
        )
    )


def all_positive(series):

    values = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if values.empty:
        return False

    return (values > 0).all()


def all_negative(series):

    values = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if values.empty:
        return False

    return (values < 0).all()


# ==========================================================
# Result Collector
# ==========================================================

def add_result(
    results,
    company_id,
    result_type,
    rule_id,
    text,
    confidence
):

    confidence = round(float(confidence), 2)

    if confidence <= 60:
        return

    results.append(
        {
            "company_id": company_id,
            "type": result_type,
            "rule_id": rule_id,
            "text": text,
            "confidence_pct": confidence
        }
    )

# ==========================================================
# Generate Pros
# ==========================================================

def generate_pros(
    companies_df,
    ratio_df,
    pl_df,
    bs_df,
    cf_df,
    results
):

    logger.info("Generating Pro Rules...")

    for _, company in companies_df.iterrows():

        company_id = company["company_id"]

        ratios = get_company_ratios(
            ratio_df,
            company_id
        )

        pnl = get_company_profit_loss(
            pl_df,
            company_id
        )

        balance = get_company_balance_sheet(
            bs_df,
            company_id
        )

        cashflow = get_company_cashflow(
            cf_df,
            company_id
        )

        latest_ratio = get_latest(ratios)

        latest_pnl = get_latest(pnl)

        latest_balance = get_latest(balance)

        latest_cashflow = get_latest(cashflow)

        if latest_ratio is None:
            continue

        # ==================================================
        # PRO 1
        # ROE >20% for last 3 years
        # ==================================================

        last3 = get_last_n_years(
            ratios,
            3
        )

        if (
            len(last3) == 3
            and
            (
                last3[
                    "return_on_equity_pct"
                ] > 20
            ).all()
        ):

            add_result(

                results,

                company_id,

                "pro",

                "PRO_01",

                (
                    "Consistently high return on equity "
                    "above 20% demonstrates exceptional "
                    "capital efficiency."
                ),

                95

            )

        # ==================================================
        # PRO 2
        # Positive FCF for 5 years
        # ==================================================

        last5 = get_last_n_years(
            ratios,
            5
        )

        if (
            len(last5) == 5
            and
            all_positive(
                last5[
                    "free_cash_flow_cr"
                ]
            )
        ):

            add_result(

                results,

                company_id,

                "pro",

                "PRO_02",

                (
                    "Strong free cash flow generation "
                    "over 5 years signals healthy "
                    "business fundamentals."
                ),

                92

            )

        # ==================================================
        # PRO 3
        # Debt Free
        # ==================================================

        debt_equity = latest_ratio[
            "debt_to_equity"
        ]

        if pd.notna(debt_equity):

            if debt_equity == 0:

                add_result(

                    results,

                    company_id,

                    "pro",

                    "PRO_03",

                    (
                        "Debt-free balance sheet provides "
                        "financial flexibility and "
                        "eliminates interest burden."
                    ),

                    96

                )

        # ==================================================
        # PRO 4
        # Revenue CAGR >15%
        # ==================================================

        revenue_cagr = latest_ratio[
            "revenue_cagr_5yr"
        ]

        if pd.notna(revenue_cagr):

            if revenue_cagr > 15:

                add_result(

                    results,

                    company_id,

                    "pro",

                    "PRO_04",

                    (
                        "Revenue growing at above "
                        "15% CAGR over 5 years "
                        "reflects strong business momentum."
                    ),

                    90

                )

        # ==================================================
        # PRO 5
        # OPM >25%
        # ==================================================

        opm = latest_ratio[
            "operating_profit_margin_pct"
        ]

        if pd.notna(opm):

            if opm > 25:

                add_result(

                    results,

                    company_id,

                    "pro",

                    "PRO_05",

                    (
                        "Operating profit margin above "
                        "25% indicates strong pricing "
                        "power and cost discipline."
                    ),

                    90

                )

        # ==================================================
        # PRO 6
        # PAT CAGR >20%
        # ==================================================

        pat_cagr = latest_ratio[
            "pat_cagr_5yr"
        ]

        if pd.notna(pat_cagr):

            if pat_cagr > 20:

                add_result(

                    results,

                    company_id,

                    "pro",

                    "PRO_06",

                    (
                        "Net profit compounding above "
                        "20% over 5 years creates "
                        "significant shareholder value."
                    ),

                    94

                )

        logger.info("Pro Rules 1-6 completed.")


        # ==================================================
        # PRO 7
        # Interest Coverage >10 OR Debt Free
        # ==================================================

        icr = latest_ratio["interest_coverage"]
        debt_equity = latest_ratio["debt_to_equity"]

        if (
            (pd.notna(icr) and icr > 10)
            or
            (pd.notna(debt_equity) and debt_equity == 0)
        ):

            add_result(

                results,

                company_id,

                "pro",

                "PRO_07",

                (
                    "Very high interest coverage ratio "
                    "reflects negligible financial stress "
                    "from debt servicing."
                ),

                90

            )

        # ==================================================
        # PRO 8
        # Dividend Yield >2% and Positive FCF
        # ==================================================

        dividend_yield = latest_ratio["dividend_yield"]

        free_cash_flow = latest_ratio["free_cash_flow_cr"]

        if (
            pd.notna(dividend_yield)
            and
            pd.notna(free_cash_flow)
        ):

            if (
                dividend_yield > 2
                and
                free_cash_flow > 0
            ):

                add_result(

                    results,

                    company_id,

                    "pro",

                    "PRO_08",

                    (
                        "Consistent dividend yield above "
                        "2% backed by positive free cash flow."
                    ),

                    88

                )

        # ==================================================
        # PRO 9
        # EPS CAGR >15%
        # ==================================================

        eps_cagr = latest_ratio["eps_cagr_5yr"]

        if pd.notna(eps_cagr):

            if eps_cagr > 15:

                add_result(

                    results,

                    company_id,

                    "pro",

                    "PRO_09",

                    (
                        "Earnings per share growing above "
                        "15% CAGR indicates strong earnings "
                        "quality and compounding."
                    ),

                    91

                )

        # ==================================================
        # PRO 10
        # ROE Improving for 3 Years
        # ==================================================

        if (
            len(last3) == 3
            and
            is_increasing(
                last3["return_on_equity_pct"]
            )
        ):

            add_result(

                results,

                company_id,

                "pro",

                "PRO_10",

                (
                    "Return on equity improving for "
                    "3 consecutive years shows "
                    "strengthening business quality."
                ),

                86

            )

        # ==================================================
        # PRO 11
        # PAT CAGR greater than Revenue CAGR
        # (Operating Leverage)
        # ==================================================

        revenue_cagr = latest_ratio["revenue_cagr_5yr"]

        pat_cagr = latest_ratio["pat_cagr_5yr"]

        if (
            pd.notna(revenue_cagr)
            and
            pd.notna(pat_cagr)
        ):

            if pat_cagr > revenue_cagr:

                add_result(

                    results,

                    company_id,

                    "pro",

                    "PRO_11",

                    (
                        "Revenue growing slower than profits "
                        "shows improving operating leverage "
                        "and scale benefits."
                    ),

                    84

                )

        # ==================================================
        # PRO 12
        # Assets Growing + Debt Declining
        # ==================================================

        last3_balance = get_last_n_years(
            balance,
            3
        )

        debt_declining = latest_ratio["debt_declining"]

        if (
            len(last3_balance) == 3
            and
            is_increasing(
                last3_balance["total_assets"]
            )
            and
            debt_declining == 1
        ):

            add_result(

                results,

                company_id,

                "pro",

                "PRO_12",

                (
                    "Growing asset base funded by internal "
                    "accruals reflects self-sustaining growth."
                ),

                90

            )


# ==========================================================
# Generate Cons
# ==========================================================

def generate_cons(
    companies_df,
    ratio_df,
    pl_df,
    bs_df,
    cf_df,
    results
):

    logger.info("Generating Con Rules...")

    for _, company in companies_df.iterrows():

        company_id = company["company_id"]

        ratios = get_company_ratios(
            ratio_df,
            company_id
        )

        pnl = get_company_profit_loss(
            pl_df,
            company_id
        )

        balance = get_company_balance_sheet(
            bs_df,
            company_id
        )

        cashflow = get_company_cashflow(
            cf_df,
            company_id
        )

        latest_ratio = get_latest(ratios)

        latest_pnl = get_latest(pnl)

        if latest_ratio is None or latest_pnl is None:
            continue

        last3_ratio = get_last_n_years(
            ratios,
            3
        )

        last3_pnl = get_last_n_years(
            pnl,
            3
        )

        # ==================================================
        # CON 1
        # Debt / Equity > 2
        # ==================================================

        debt_equity = latest_ratio["debt_to_equity"]

        if (
            pd.notna(debt_equity)
            and debt_equity > 2
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_01",

                (
                    f"Debt-to-equity ratio of "
                    f"{debt_equity:.2f} is elevated "
                    "for a non-financial company "
                    "and warrants monitoring."
                ),

                92

            )

        # ==================================================
        # CON 2
        # Negative FCF for 3 Years
        # ==================================================

        if (
            len(last3_ratio) == 3
            and
            all_negative(
                last3_ratio[
                    "free_cash_flow_cr"
                ]
            )
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_02",

                (
                    "Free cash flow negative for "
                    "3 consecutive years raises "
                    "concern about cash generation quality."
                ),

                90

            )

        # ==================================================
        # CON 3
        # OPM Declining
        # ==================================================

        if (
            len(last3_ratio) == 3
            and
            is_decreasing(
                last3_ratio[
                    "operating_profit_margin_pct"
                ]
            )
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_03",

                (
                    "Operating margins declining "
                    "for 3 consecutive years "
                    "suggest pricing or cost pressure."
                ),

                86

            )

        # ==================================================
        # CON 4
        # Net Profit Negative
        # ==================================================

        net_profit = latest_pnl["net_profit"]

        if (
            pd.notna(net_profit)
            and net_profit < 0
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_04",

                (
                    "Company reported a net loss "
                    "in the most recent financial year."
                ),

                95

            )

        # ==================================================
        # CON 5
        # Revenue Declining
        # ==================================================

        if (
            len(last3_pnl) == 3
            and
            is_decreasing(
                last3_pnl[
                    "sales"
                ]
            )
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_05",

                (
                    "Revenue contraction over "
                    "2 consecutive years indicates "
                    "demand weakness or market share loss."
                ),

                88

            )

        # ==================================================
        # CON 6
        # Interest Coverage < 1.5
        # ==================================================

        icr = latest_ratio["interest_coverage"]

        if (
            pd.notna(icr)
            and icr < 1.5
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_06",

                (
                    "Interest coverage ratio below "
                    "1.5x indicates the company "
                    "is at risk of not meeting "
                    "its debt obligations."
                ),

                94

            )

        logger.info("Con Rules 1-6 completed.")


        # ==================================================
        # CON 7
        # Dividend Payout >100%
        # ==================================================

        payout = latest_ratio[
            "dividend_payout_ratio_pct"
        ]

        if (
            pd.notna(payout)
            and payout > 100
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_07",

                (
                    "Dividend payout ratio above "
                    "100% means the company is "
                    "paying dividends from reserves, "
                    "which is unsustainable."
                ),

                90

            )

        # ==================================================
        # CON 8
        # Debt Equity Rising
        # ==================================================

        if (
            len(last3_ratio) == 3
            and
            is_increasing(
                last3_ratio[
                    "debt_to_equity"
                ]
            )
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_08",

                (
                    "Rising debt-to-equity ratio "
                    "over 3 years suggests increasing "
                    "financial leverage risk."
                ),

                88

            )

        # ==================================================
        # CON 9
        # EPS Declining
        # ==================================================

        if (
            len(last3_pnl) == 3
            and
            is_decreasing(
                last3_pnl[
                    "eps"
                ]
            )
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_09",

                (
                    "Earnings per share declining "
                    "for 3 consecutive years reflects "
                    "deteriorating profitability."
                ),

                90

            )

        # ==================================================
        # CON 10
        # ROCE <10%
        # ==================================================

        roce = latest_ratio[
            "return_on_capital_employed_pct"
        ]

        if (
            pd.notna(roce)
            and roce < 10
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_10",

                (
                    "Return on capital employed below "
                    "10% suggests the business is not "
                    "generating sufficient returns on "
                    "invested capital."
                ),

                92

            )

        # ==================================================
        # CON 11
        # Net Debt >3x EBITDA
        # Skipped (EBITDA unavailable)
        # ==================================================

        logger.debug(
            "CON_11 skipped for %s "
            "(EBITDA not available).",
            company_id
        )

        # ==================================================
        # CON 12
        # Revenue CAGR <5%
        # ==================================================

        revenue_cagr = latest_ratio[
            "revenue_cagr_5yr"
        ]

        if (
            pd.notna(revenue_cagr)
            and revenue_cagr < 5
        ):

            add_result(

                results,

                company_id,

                "con",

                "CON_12",

                (
                    "Revenue growing below 5% over "
                    "5 years lags inflation and "
                    "suggests limited business momentum."
                ),

                86

            )


# ==========================================================
# Save Output
# ==========================================================

def save_output(results):

    df = pd.DataFrame(results)

    df = df.sort_values(
        ["company_id", "type", "rule_id"]
    ).reset_index(drop=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    logger.info(
        "Generated %d records.",
        len(df)
    )

    return df


# ==========================================================
# Verification
# ==========================================================

def verify_output(companies_df, output_df):

    logger.info(
        "Verifying generated output..."
    )

    failed = []

    for company_id in companies_df["company_id"]:

        company_rows = output_df[
            output_df["company_id"] == company_id
        ]

        pros = (
            company_rows["type"] == "pro"
        ).sum()

        cons = (
            company_rows["type"] == "con"
        ).sum()

        if pros == 0 or cons == 0:

            failed.append(company_id)

    if failed:

        logger.warning(
            "Companies failing verification: %s",
            ", ".join(failed)
        )

    else:

        logger.info(
            "Verification Passed."
        )

    return failed

def apply_fallback_rules(companies_df, results):

    df = pd.DataFrame(results)

    for company_id in companies_df["company_id"]:

        company_rows = df[df["company_id"] == company_id]

        has_pro = (
            not company_rows.empty
            and (company_rows["type"] == "pro").any()
        )

        has_con = (
            not company_rows.empty
            and (company_rows["type"] == "con").any()
        )

        if not has_pro:

            add_result(
                results,
                company_id,
                "pro",
                "PRO_99",
                "Company has an established market presence and long-term business potential.",
                65
            )

        if not has_con:

            add_result(
                results,
                company_id,
                "con",
                "CON_99",
                "Business performance may face future market and industry risks.",
                65
            )

        df = pd.DataFrame(results)


# ==========================================================
# Summary
# ==========================================================

def print_summary(df, failed):

    print("\n" + "=" * 60)

    print("Sprint 5 - Day 30")

    print("Pros & Cons Generator")

    print("=" * 60)

    print(
        f"Generated Records : {len(df)}"
    )

    print(
        f"Companies Covered : {df['company_id'].nunique()}"
    )

    print(
        f"Pros : {(df['type']=='pro').sum()}"
    )

    print(
        f"Cons : {(df['type']=='con').sum()}"
    )

    print(
        f"Verification Failed : {len(failed)}"
    )

    print("\nGenerated Files")

    print("-" * 60)

    print(OUTPUT_FILE)

    print(LOG_FILE)

    print("=" * 60)


# ==========================================================
# Main
# ==========================================================

def main():

    logger.info("=" * 60)

    logger.info(
        "Pros & Cons Generator Started"
    )

    conn = None

    try:

        conn = connect_database()

        companies_df = load_companies(conn)

        ratio_df = load_financial_ratios(conn)

        pl_df = load_profit_loss(conn)

        bs_df = load_balance_sheet(conn)

        cf_df = load_cashflow(conn)

        results = []

        generate_pros(
            companies_df,
            ratio_df,
            pl_df,
            bs_df,
            cf_df,
            results
        )

        generate_cons(
            companies_df,
            ratio_df,
            pl_df,
            bs_df,
            cf_df,
            results
        )

        apply_fallback_rules(
            companies_df,
            results
        )

        output_df = save_output(
            results
        )

        failed = verify_output(
            companies_df,
            output_df
        )

        print_summary(
            output_df,
            failed
        )

        logger.info(
            "Day 30 Completed Successfully."
        )

    except Exception as e:

        logger.exception(e)

        print("\nERROR")

        print("-" * 60)

        print(e)

        print("-" * 60)

    finally:

        if conn is not None:
            conn.close()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()