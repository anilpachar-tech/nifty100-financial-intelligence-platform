import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    SimpleDocTemplate,
    PageBreak
)

from tearsheet import connect_database

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = PROJECT_ROOT / "reports" / "sector"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

styles = getSampleStyleSheet()

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    spaceAfter=16
)

sub_heading = ParagraphStyle(
    "SubHeading",
    parent=styles["Heading2"],
    spaceAfter=10
)

# ==========================================================
# Sector Loader
# ==========================================================

def get_all_sectors(conn):

    query = """
    SELECT DISTINCT broad_sector
    FROM sectors
    WHERE broad_sector IS NOT NULL
    ORDER BY broad_sector
    """

    df = pd.read_sql(query, conn)

    return df["broad_sector"].tolist()

# ==========================================================
# Company Loader
# ==========================================================

def load_sector_companies(
    conn,
    sector
):

    query = """
    SELECT

        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector

    FROM companies c

    INNER JOIN sectors s

        ON c.id=s.company_id

    WHERE s.broad_sector=?

    ORDER BY c.id
    """

    return pd.read_sql(

        query,

        conn,

        params=[sector]

    )

# ==========================================================
# Latest Financial Ratios
# ==========================================================

def load_latest_ratios(conn):

    query = """
    SELECT *

    FROM financial_ratios
    """

    df = pd.read_sql(query, conn)

    if df.empty:

        return df

    df["year"] = (

        df["year"]

        .astype(str)

        .str.extract(r"(\d+)")

        .astype(float)

    )

    df = (

        df

        .sort_values("year")

        .groupby("company_id")

        .tail(1)

    )

    return df

# ==========================================================
# Sector KPI Summary
# ==========================================================

def sector_summary(

    ratios,

    companies

):

    merged = companies.merge(

        ratios,

        left_on="id",

        right_on="company_id",

        how="left"

    )

    summary = {

        "Median ROE":

        merged[
            "return_on_equity_pct"
        ].median(),

        "Median ROCE":

        merged[
            "return_on_capital_employed_pct"
        ].median(),

        "Median PE":

        merged[
            "pe"
        ].median(),

        "Median Debt/Equity":

        merged[
            "debt_to_equity"
        ].median()

    }

    return summary

# ==========================================================
# Company Table
# ==========================================================

def build_company_table(companies, ratios):

    merged = companies.merge(
        ratios,
        left_on="id",
        right_on="company_id",
        how="left"
    )

    table_data = [[
        "Ticker",
        "Company",
        "ROE",
        "ROCE",
        "PE",
        "Debt/Eq",
        "Current",
        "EPS",
        "Book Value",
        "Div Yield"
    ]]

    for _, row in merged.iterrows():

        ticker = row["id_x"] if "id_x" in row else row["id"]

        roe = (
            "-"
            if pd.isna(row["return_on_equity_pct"])
            else round(row["return_on_equity_pct"], 2)
        )

        roce = (
            "-"
            if pd.isna(row["return_on_capital_employed_pct"])
            else round(row["return_on_capital_employed_pct"], 2)
        )

        pe = (
            "-"
            if pd.isna(row["pe"])
            else round(row["pe"], 2)
        )

        debt = (
            "-"
            if pd.isna(row["debt_to_equity"])
            else round(row["debt_to_equity"], 2)
        )

        current_ratio = "-"

        eps = (
            "-"
            if pd.isna(row["earnings_per_share"])
            else round(row["earnings_per_share"], 2)
        )

        book = (
            "-"
            if pd.isna(row["book_value_per_share"])
            else round(row["book_value_per_share"], 2)
        )

        dividend = (
            "-"
            if pd.isna(row["dividend_yield"])
            else round(row["dividend_yield"], 2)
        )

        table_data.append([
            ticker,
            row["company_name"],
            roe,
            roce,
            pe,
            debt,
            current_ratio,
            eps,
            book,
            dividend
        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),0.4,colors.black),

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#D9EAD3")),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),8),

        ("FONTSIZE",(0,0),(-1,-1),8)

    ]))

    return table

# ==========================================================
# Build Sector PDF
# ==========================================================

def build_sector_pdf(conn, sector):

    companies = load_sector_companies(conn, sector)

    ratios = load_latest_ratios(conn)

    summary = sector_summary(
        ratios,
        companies
    )

    pdf_path = REPORT_DIR / f"{sector}_report.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        rightMargin=25,
        leftMargin=25,
        topMargin=30,
        bottomMargin=30
    )

    elements = []

    # -------------------------------
    # Title
    # -------------------------------

    elements.append(
        Paragraph(
            f"{sector} Sector Report",
            heading_style
        )
    )

    elements.append(
        Spacer(1, 0.20 * inch)
    )

    elements.append(
        Paragraph(
            f"<b>Total Companies:</b> {len(companies)}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 0.20 * inch)
    )

    # -------------------------------
    # Summary Table
    # -------------------------------

    summary_rows = [["Metric", "Median"]]

    for metric, value in summary.items():

        if pd.isna(value):
            display = "-"
        else:
            display = f"{value:.2f}"

        summary_rows.append([
            metric,
            display
        ])

    summary_table = Table(
        summary_rows,
        colWidths=[260, 120]
    )

    summary_table.setStyle(TableStyle([

        ("GRID", (0,0), (-1,-1), 0.4, colors.black),

        ("BACKGROUND", (0,0), (-1,0),
         colors.HexColor("#D9EAD3")),

        ("FONTNAME", (0,0), (-1,0),
         "Helvetica-Bold"),

        ("ALIGN", (0,0), (-1,-1),
         "CENTER"),

        ("BOTTOMPADDING", (0,0), (-1,0), 8)

    ]))

    elements.append(summary_table)

    elements.append(
        Spacer(1, 0.35 * inch)
    )

    elements.append(
        Paragraph(
            "Company Financial Snapshot",
            sub_heading
        )
    )

    elements.append(
        build_company_table(
            companies,
            ratios
        )
    )

    doc.build(elements)

    print(f"Generated : {pdf_path.name}")


# ==========================================================
# Generate All Sector Reports
# ==========================================================

def generate_all_sector_reports(conn):

    # Remove old reports
    for pdf in REPORT_DIR.glob("*_report.pdf"):
        pdf.unlink()

    sectors = get_all_sectors(conn)

    generated = 0

    print()
    print("=" * 60)
    print("Generating Sector Reports")
    print("=" * 60)

    for sector in sectors:

        print(f"Generating : {sector}")

        try:

            build_sector_pdf(
                conn,
                sector
            )

            generated += 1

        except Exception as e:

            print(f"Failed : {sector}")
            print(e)

    return generated


# ==========================================================
# Validation
# ==========================================================

def validate_sector_reports(expected_count):

    pdf_files = sorted(
        REPORT_DIR.glob("*_report.pdf")
    )

    print()
    print("=" * 60)
    print("Validation")
    print("=" * 60)

    print(f"Expected : {expected_count}")
    print(f"Generated: {len(pdf_files)}")

    if len(pdf_files) == expected_count:

        print("Status    : PASS")

    else:

        print("Status    : FAIL")

    print()

    for pdf in pdf_files:

        size = round(pdf.stat().st_size / 1024, 2)

        print(f"{pdf.name}  ({size} KB)")


# ==========================================================
# Main
# ==========================================================

def main():

    conn = connect_database()

    try:

        total = generate_all_sector_reports(conn)

        validate_sector_reports(total)

        print()
        print("=" * 60)
        print("Day 34 Completed")
        print("=" * 60)
        print(f"Sector Reports Generated : {total}")

    finally:

        conn.close()


if __name__ == "__main__":

    main()

