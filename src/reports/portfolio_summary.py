import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from tearsheet import connect_database


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = PROJECT_ROOT / "reports" / "portfolio"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

styles = getSampleStyleSheet()

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    spaceAfter=18
)

sub_heading = ParagraphStyle(
    "SubHeading",
    parent=styles["Heading2"],
    spaceAfter=10
)


# ==========================================================
# Company Loader
# ==========================================================

def load_companies(conn):

    query = """
    SELECT

        c.id,
        c.company_name,
        s.broad_sector

    FROM companies c

    LEFT JOIN sectors s

        ON c.id = s.company_id

    ORDER BY c.id
    """

    return pd.read_sql(query, conn)


# ==========================================================
# Financial Ratios Loader
# ==========================================================

def load_financial_ratios(conn):

    query = """
    SELECT *

    FROM financial_ratios
    """

    df = pd.read_sql(query, conn)

    df["year"] = (

        df["year"]

        .astype(str)

        .str.extract(r"(\d+)")

        .astype(float)

    )

    df = df.sort_values(

        ["company_id", "year"]

    )

    return df


# ==========================================================
# Trend Arrow
# ==========================================================

def trend_arrow(previous, latest):

    if pd.isna(previous) or pd.isna(latest):

        return "→"

    if latest > previous * 1.02:

        return "↑"

    elif latest < previous * 0.98:

        return "↓"

    else:

        return "→"


# ==========================================================
# Latest + Previous Record
# ==========================================================

def latest_previous(df, company):

    company_df = df[

        df["company_id"] == company

    ]

    if len(company_df) == 0:

        return None, None

    latest = company_df.iloc[-1]

    if len(company_df) >= 2:

        previous = company_df.iloc[-2]

    else:

        previous = latest

    return latest, previous

# ==========================================================
# Build Company Page
# ==========================================================

def build_company_page(elements, company, ratios):

    latest, previous = latest_previous(
        ratios,
        company["id"]
    )

    elements.append(
        Paragraph(
            company["company_name"],
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Ticker :</b> {company['id']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Sector :</b> {company['broad_sector']}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 0.25 * inch)
    )

    if latest is None:

        elements.append(
            Paragraph(
                "No Financial Data Available",
                styles["Normal"]
            )
        )

        elements.append(PageBreak())

        return

    metrics = [

        (
            "ROE",
            latest["return_on_equity_pct"],
            trend_arrow(
                previous["return_on_equity_pct"],
                latest["return_on_equity_pct"]
            )
        ),

        (
            "ROCE",
            latest["return_on_capital_employed_pct"],
            trend_arrow(
                previous["return_on_capital_employed_pct"],
                latest["return_on_capital_employed_pct"]
            )
        ),

        (
            "PE",
            latest["pe"],
            trend_arrow(
                previous["pe"],
                latest["pe"]
            )
        ),

        (
            "Debt / Equity",
            latest["debt_to_equity"],
            trend_arrow(
                previous["debt_to_equity"],
                latest["debt_to_equity"]
            )
        ),

        (
            "EPS",
            latest["earnings_per_share"],
            trend_arrow(
                previous["earnings_per_share"],
                latest["earnings_per_share"]
            )
        ),

        (
            "Dividend Yield",
            latest["dividend_yield"],
            trend_arrow(
                previous["dividend_yield"],
                latest["dividend_yield"]
            )
        )

    ]

    table_data = [

        [
            "Metric",
            "Latest",
            "Trend"
        ]

    ]

    for metric, value, arrow in metrics:

        if pd.isna(value):

            value = "-"

        else:

            value = round(value, 2)

        table_data.append(

            [
                metric,
                value,
                arrow
            ]

        )

    table = Table(

        table_data,

        colWidths=[3.0 * inch, 1.3 * inch, 1.0 * inch]

    )

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#D9EAD3")),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,0),8),

            ("FONTSIZE",(0,0),(-1,-1),10)

        ])

    )

    elements.append(table)

    elements.append(
        Spacer(1, 0.40 * inch)
    )

    elements.append(

        Paragraph(

            "<b>Generated by</b><br/>"
            "Nifty100 Financial Intelligence Platform",

            styles["Normal"]

        )

    )

    elements.append(
        PageBreak()
    )

# ==========================================================
# Build Portfolio PDF
# ==========================================================

def build_portfolio_pdf():

    conn = connect_database()

    companies = load_companies(conn)

    ratios = load_financial_ratios(conn)

    pdf_path = REPORT_DIR / "portfolio_summary.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []

    print()
    print("=" * 60)
    print("Generating Portfolio Summary")
    print("=" * 60)

    total = len(companies)

    for index, (_, company) in enumerate(companies.iterrows(), start=1):

        print(f"[{index}/{total}] {company['id']}")

        build_company_page(
            elements,
            company,
            ratios
        )

    doc.build(elements)

    conn.close()

    return pdf_path


# ==========================================================
# Validation
# ==========================================================

def validate_portfolio(pdf_path):

    print()
    print("=" * 60)
    print("Portfolio Validation")
    print("=" * 60)

    if pdf_path.exists():

        size = round(
            pdf_path.stat().st_size / 1024,
            2
        )

        print(f"File : {pdf_path.name}")
        print(f"Size : {size} KB")

        if size > 0:

            print("Status : PASS")

        else:

            print("Status : FAIL")

    else:

        print("Portfolio PDF not found")


# ==========================================================
# Main
# ==========================================================

def main():

    pdf_path = build_portfolio_pdf()

    validate_portfolio(pdf_path)

    print()
    print("=" * 60)
    print("Sprint 5 - Day 35 Completed")
    print("=" * 60)


if __name__ == "__main__":

    main()