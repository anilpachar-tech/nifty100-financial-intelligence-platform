"""
Sprint 2 - Day 11

Cash Flow KPI Engine
"""

from typing import Optional


def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow

    Formula

    CFO + CFI

    Negative values
    are allowed.
    """

    return round(
        operating_activity +
        investing_activity,
        2
    )

def cfo_quality_score(
    average_cfo: float,
    average_pat: float
) -> tuple[Optional[float], Optional[str]]:
    """
    CFO Quality Score

    Formula

    Average CFO /
    Average PAT

    Returns

    (
        score,
        quality_label
    )
    """

    if average_pat == 0:
        return None, None

    score = round(
        average_cfo /
        average_pat,
        2
    )

    if score > 1.0:
        label = "High Quality"

    elif score >= 0.5:
        label = "Moderate"

    else:
        label = "Accrual Risk"

    return score, label

def capex_intensity(
    investing_activity: float,
    sales: float
) -> tuple[Optional[float], Optional[str]]:
    """
    CapEx Intensity

    Formula

    abs(CFI) / Sales * 100

    Returns

    (
        percentage,
        category
    )
    """

    if sales == 0:
        return None, None

    intensity = round(
        (
            abs(investing_activity) /
            sales
        ) * 100,
        2
    )

    if intensity < 3:
        category = "Asset Light"

    elif intensity <= 8:
        category = "Moderate"

    else:
        category = "Capital Intensive"

    return intensity, category

def fcf_conversion_rate(
    free_cash_flow: float,
    operating_profit: float
) -> tuple[Optional[float], Optional[str]]:
    """
    Free Cash Flow Conversion Rate

    Formula

    FCF / Operating Profit * 100

    Returns

    (
        conversion_rate,
        status
    )
    """

    if operating_profit == 0:
        return None, None

    conversion = round(
        (
            free_cash_flow /
            operating_profit
        ) * 100,
        2
    )

    if conversion >= 100:
        status = "Excellent"

    elif conversion >= 70:
        status = "Good"

    else:
        status = "Weak"

    return conversion, status

def capital_allocation_pattern(
    operating_activity: float,
    investing_activity: float,
    financing_activity: float,
    cfo_pat_ratio: Optional[float] = None
) -> str:
    """
    Capital Allocation Pattern Classifier

    Returns one of the predefined
    business pattern labels.
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    # (+,-,-)
    if cfo == "+" and cfi == "-" and cff == "-":

        if (
            cfo_pat_ratio is not None and
            cfo_pat_ratio > 1.0
        ):
            return "Shareholder Returns"

        return "Reinvestor"

    # (+,+,-)
    if cfo == "+" and cfi == "+" and cff == "-":
        return "Liquidating Assets"

    # (-,+,+)
    if cfo == "-" and cfi == "+" and cff == "+":
        return "Distress Signal"

    # (-,-,+)
    if cfo == "-" and cfi == "-" and cff == "+":
        return "Growth Funded by Debt"

    # (+,+,+)
    if cfo == "+" and cfi == "+" and cff == "+":
        return "Cash Accumulator"

    # (-,-,-)
    if cfo == "-" and cfi == "-" and cff == "-":
        return "Pre-Revenue"

    # (+,-,+)
    if cfo == "+" and cfi == "-" and cff == "+":
        return "Mixed"

    return "Other"


# =====================================================
# Sprint 5 - Day 31
# Cash Flow Intelligence Module
# =====================================================

import logging
import sqlite3
from pathlib import Path

import pandas as pd


# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(
    exist_ok=True
)

EXCEL_OUTPUT = (
    OUTPUT_DIR /
    "cashflow_intelligence.xlsx"
)

DISTRESS_OUTPUT = (
    OUTPUT_DIR /
    "distress_alerts.csv"
)

LOG_FILE = (
    OUTPUT_DIR /
    "cashflow_kpis.log"
)


# =====================================================
# Logging
# =====================================================

logging.basicConfig(

    filename=LOG_FILE,

    level=logging.INFO,

    format=(
        "%(asctime)s "
        "%(levelname)s "
        "%(message)s"
    )

)

logger = logging.getLogger(__name__)


# =====================================================
# Database Connection
# =====================================================

def connect_database():

    logger.info(
        "Connecting to database..."
    )

    return sqlite3.connect(DB_FILE)

# =====================================================
# Data Loaders
# =====================================================

def load_companies(conn):

    query = """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    ORDER BY id
    """

    logger.info(
        "Loading companies..."
    )

    return pd.read_sql(
        query,
        conn
    )


def load_sectors(conn):

    query = """
    SELECT *
    FROM sectors
    """

    logger.info(
        "Loading sectors..."
    )

    return pd.read_sql(
        query,
        conn
    )


def load_cashflow(conn):

    query = """
    SELECT *
    FROM cashflow
    """

    logger.info(
        "Loading cashflow..."
    )

    return pd.read_sql(
        query,
        conn
    )


def load_profit_loss(conn):

    query = """
    SELECT *
    FROM profitandloss
    """

    logger.info(
        "Loading profit & loss..."
    )

    return pd.read_sql(
        query,
        conn
    )


def load_balance_sheet(conn):

    query = """
    SELECT *
    FROM balancesheet
    """

    logger.info(
        "Loading balance sheet..."
    )

    return pd.read_sql(
        query,
        conn
    )


def load_financial_ratios(conn):

    query = """
    SELECT *
    FROM financial_ratios
    """

    logger.info(
        "Loading financial ratios..."
    )

    return pd.read_sql(
        query,
        conn
    )

# =====================================================
# Helper Functions
# =====================================================

def get_latest(df):

    if df.empty:
        return pd.Series(dtype="object")

    return df.iloc[0]


def get_last_5_years(df):

    if df.empty:
        return df

    return df.head(5)


def safe_average(series):

    series = series.dropna()

    if series.empty:
        return None

    return round(
        series.mean(),
        2
    )


def safe_value(value):

    if pd.isna(value):
        return None

    return value


def get_company_cashflow(
    cashflow_df,
    company_id
):

    df = cashflow_df[
        cashflow_df["company_id"] == company_id
    ].copy()

    return df.reset_index(
        drop=True
    )


def get_company_profit_loss(
    profit_loss_df,
    company_id
):

    df = profit_loss_df[
        profit_loss_df["company_id"] == company_id
    ].copy()

    return df.reset_index(
        drop=True
    )


def get_company_balance_sheet(
    balance_sheet_df,
    company_id
):

    df = balance_sheet_df[
        balance_sheet_df["company_id"] == company_id
    ].copy()

    return df.reset_index(
        drop=True
    )


def get_company_ratios(
    ratios_df,
    company_id
):

    df = ratios_df[
        ratios_df["company_id"] == company_id
    ].copy()

    return df.reset_index(
        drop=True
    )


def get_company_sector(
    sectors_df,
    company_id
):

    df = sectors_df[
        sectors_df["company_id"] == company_id
    ]

    if df.empty:
        return None

    return df.iloc[0]["broad_sector"]

# =====================================================
# Cash Flow Intelligence Generator
# =====================================================

def generate_cashflow_intelligence(

    companies_df,
    sectors_df,
    cashflow_df,
    profit_loss_df,
    balance_sheet_df,
    ratios_df

):

    logger.info(
        "Generating Cash Flow Intelligence..."
    )

    results = []

    distress_results = []

    for _, company in companies_df.iterrows():

        company_id = company["company_id"]

        sector = get_company_sector(
            sectors_df,
            company_id
        )

        company_cf = get_company_cashflow(
            cashflow_df,
            company_id
        )

        company_pl = get_company_profit_loss(
            profit_loss_df,
            company_id
        )

        company_bs = get_company_balance_sheet(
            balance_sheet_df,
            company_id
        )

        company_ratio = get_company_ratios(
            ratios_df,
            company_id
        )

        if company_pl.empty:
            continue

        if company_cf.empty:

            results.append({

                "company_id": company_id,
                "sector": sector,

                "cfo_quality_score": None,
                "cfo_quality_lable": None,

                "capex_intensity_pct": None,
                "capex_lable": None,

                "fcf_cagr_5yr": None,
                "fcf_conversion_pct": None,

                "distress_flag": False,
                "deleveraging_flag": False,

                "capital_allocation_label": "Cash Flow Data Missing"

            })

            continue

        latest_cf = get_latest(
            company_cf
        )

        latest_pl = get_latest(
            company_pl
        )

        latest_bs = get_latest(
            company_bs
        ) if not company_bs.empty else pd.Series(dtype="object")

        latest_ratio = get_latest(
            company_ratio
        ) if not company_ratio.empty else pd.Series(dtype="object")

        last5_cf = get_last_5_years(
            company_cf
        )

        last5_pl = get_last_5_years(
            company_pl
        )

        # ==========================================
        # CFO Quality
        # ==========================================

        avg_cfo = safe_average(
            last5_cf[
                "operating_activity"
            ]
        )

        avg_pat = safe_average(
            last5_pl[
                "net_profit"
            ]
        )

        cfo_score, cfo_label = (
            cfo_quality_score(
                avg_cfo,
                avg_pat
            )
            if (
                avg_cfo is not None and
                avg_pat is not None
            )
            else (None, None)
        )

        # ==========================================
        # CapEx Intensity
        # ==========================================

        capex_pct, capex_label = (
            capex_intensity(

                latest_cf[
                    "investing_activity"
                ],

                latest_pl[
                    "sales"
                ]

            )
        )

        # ==========================================
        # Free Cash Flow
        # ==========================================

        latest_fcf = free_cash_flow(

            latest_cf[
                "operating_activity"
            ],

            latest_cf[
                "investing_activity"
            ]

        )

        fcf_conversion, _ = (
            fcf_conversion_rate(

                latest_fcf,

                latest_pl[
                    "operating_profit"
                ]

            )
        )


        # ==========================================
        # FCF CAGR (Latest Ratio)
        # ==========================================

        fcf_cagr = safe_value(
            latest_ratio.get(
                "revenue_cagr_5yr"
            )
        )

        # ==========================================
        # Distress Signal
        # CFO < 0 and CFF > 0
        # ==========================================

        distress_flag = False

        if (

            latest_cf[
                "operating_activity"
            ] < 0

            and

            latest_cf[
                "financing_activity"
            ] > 0

        ):

            distress_flag = True

            distress_results.append({

                "company_id": company_id,

                "cfo_value":
                    latest_cf[
                        "operating_activity"
                    ],

                "cff_value":
                    latest_cf[
                        "financing_activity"
                    ],

                "latest_net_profit":
                    latest_pl[
                        "net_profit"
                    ]

            })

        # ==========================================
        # Deleveraging Flag
        # ==========================================

        deleveraging_flag = False

        if (
            len(company_bs) >= 2
        ):

            latest_borrowing = (
                company_bs.iloc[0][
                    "borrowings"
                ]
            )

            previous_borrowing = (
                company_bs.iloc[1][
                    "borrowings"
                ]
            )

            if (

                latest_cf[
                    "financing_activity"
                ] < 0

                and

                latest_borrowing <
                previous_borrowing

            ):

                deleveraging_flag = True

        # ==========================================
        # Capital Allocation Label
        # ==========================================

        capital_label = (
            capital_allocation_pattern(

                latest_cf[
                    "operating_activity"
                ],

                latest_cf[
                    "investing_activity"
                ],

                latest_cf[
                    "financing_activity"
                ],

                cfo_score

            )
        )

        # ==========================================
        # Final Output Record
        # ==========================================

        results.append({

            "company_id":
                company_id,

            "sector":
                sector,

            "cfo_quality_score":
                cfo_score,

            "cfo_quality_label":
                cfo_label,

            "capex_intensity_pct":
                capex_pct,

            "capex_label":
                capex_label,

            "fcf_cagr_5yr":
                fcf_cagr,

            "fcf_conversion_pct":
                fcf_conversion,

            "distress_flag":
                distress_flag,

            "deleveraging_flag":
                deleveraging_flag,

            "capital_allocation_label":
                capital_label

        })

    logger.info(
        "Cash Flow Intelligence Generated "
        "for %d companies.",
        len(results)
    )

    return (

        pd.DataFrame(results),

        pd.DataFrame(distress_results)

    )

# =====================================================
# Save Outputs
# =====================================================

def save_outputs(

    intelligence_df,
    distress_df

):

    intelligence_df.to_excel(

        EXCEL_OUTPUT,

        index=False

    )

    distress_df.to_csv(

        DISTRESS_OUTPUT,

        index=False

    )

    logger.info(
        "Cash Flow Intelligence saved."
    )

    logger.info(
        "Distress Alerts saved."
    )


# =====================================================
# Summary
# =====================================================

def print_summary(

    intelligence_df,
    distress_df

):

    print("\n" + "=" * 60)

    print(
        "Sprint 5 - Day 31"
    )

    print(
        "Cash Flow Intelligence Module"
    )

    print("=" * 60)

    print(

        f"Companies Processed : "
        f"{len(intelligence_df)}"

    )

    print(

        f"Distress Alerts : "
        f"{len(distress_df)}"

    )

    print("\nGenerated Files")

    print("-" * 60)

    print(EXCEL_OUTPUT)

    print(DISTRESS_OUTPUT)

    print(LOG_FILE)

    print("=" * 60)


# =====================================================
# Main
# =====================================================

def main():

    logger.info(
        "=" * 60
    )

    logger.info(
        "Day 31 Started"
    )

    conn = None

    try:

        conn = connect_database()

        companies_df = load_companies(
            conn
        )

        sectors_df = load_sectors(
            conn
        )

        cashflow_df = load_cashflow(
            conn
        )

        profit_loss_df = (
            load_profit_loss(
                conn
            )
        )

        balance_sheet_df = (
            load_balance_sheet(
                conn
            )
        )

        ratios_df = (
            load_financial_ratios(
                conn
            )
        )

        intelligence_df, distress_df = (

            generate_cashflow_intelligence(

                companies_df,

                sectors_df,

                cashflow_df,

                profit_loss_df,

                balance_sheet_df,

                ratios_df

            )

        )

        save_outputs(

            intelligence_df,

            distress_df

        )

        print_summary(

            intelligence_df,

            distress_df

        )

        logger.info(
            "Day 31 Completed Successfully."
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


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    main()