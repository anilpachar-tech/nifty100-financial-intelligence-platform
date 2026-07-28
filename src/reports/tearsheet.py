import logging
import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_DIR = OUTPUT_DIR / "tearsheets"

LOG_FILE = OUTPUT_DIR / "tearsheet.log"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# =====================================================
# Database
# =====================================================


def connect_database():

    logger.info("Connecting database...")

    return sqlite3.connect(DB_FILE)


# =====================================================
# PDF Constants
# =====================================================

PAGE_WIDTH = 8.27 * inch

PAGE_HEIGHT = 11.69 * inch

LEFT_MARGIN = 0.50 * inch

RIGHT_MARGIN = 0.50 * inch

TOP_MARGIN = 0.50 * inch

BOTTOM_MARGIN = 0.50 * inch


# =====================================================
# Colors
# =====================================================

NAVY = colors.HexColor("#0B3C6D")

LIGHT_BLUE = colors.HexColor("#EAF3FF")

GREEN = colors.HexColor("#2E8B57")

RED = colors.HexColor("#C0392B")

GRAY = colors.HexColor("#666666")

LIGHT_GRAY = colors.HexColor("#F3F3F3")

WHITE = colors.white


# =====================================================
# Styles
# =====================================================

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "Title",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    fontSize=20,
    textColor=WHITE,
    spaceAfter=6,
)

HEADING_STYLE = ParagraphStyle(
    "Heading", parent=styles["Heading2"], fontSize=13, textColor=NAVY, spaceAfter=6
)

NORMAL_STYLE = ParagraphStyle(
    "Normal", parent=styles["BodyText"], fontSize=9, leading=12
)

SMALL_STYLE = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=8, leading=10)


# =====================================================
# PDF Canvas
# =====================================================


def create_canvas(company_id):

    output_file = REPORT_DIR / f"{company_id}_tearsheet.pdf"

    pdf = canvas.Canvas(str(output_file), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    logger.info("Creating PDF : %s", company_id)

    return pdf, output_file


# =====================================================
# Company Details
# =====================================================


def load_company(conn, company_id):

    query = """
    SELECT *
    FROM companies
    WHERE UPPER(id)=?
    """

    df = pd.read_sql(query, conn, params=[company_id.upper()])

    if df.empty:
        return None

    return df.iloc[0]


# =====================================================
# Profit & Loss
# =====================================================


def load_profit_loss(conn, company_id):

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[company_id])

    return df


# =====================================================
# Balance Sheet
# =====================================================


def load_balance_sheet(conn, company_id):

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[company_id])

    return df


# =====================================================
# Cash Flow
# =====================================================


def load_cashflow(conn, company_id):

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[company_id])

    return df


# =====================================================
# Financial Ratios
# =====================================================


def load_financial_ratios(conn, company_id):

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[company_id])

    return df


# =====================================================
# Pros & Cons
# =====================================================


def load_pros_cons(conn, company_id):

    query = """
    SELECT *
    FROM prosandcons
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[company_id])

    return df


# =====================================================
# Capital Allocation
# =====================================================


def load_capital_allocation(company_id):

    file_path = OUTPUT_DIR / "capital_allocation.csv"

    df = pd.read_csv(file_path)

    df["company_id"] = df["company_id"].astype(str).str.upper().str.strip()

    company_df = df[df["company_id"] == company_id.upper()].copy()

    return company_df


# =====================================================
# Cashflow Intelligence
# =====================================================


def load_cashflow_intelligence(company_id):

    file_path = OUTPUT_DIR / "cashflow_intelligence.xlsx"

    df = pd.read_excel(file_path)

    df["company_id"] = df["company_id"].astype(str).str.upper().str.strip()

    company_df = df[df["company_id"] == company_id.upper()].copy()

    return company_df


# =====================================================
# Latest Record
# =====================================================


def latest_record(df):

    if df.empty:
        return pd.Series(dtype="object")

    df = df.copy()

    df = df.dropna(subset=["year"])

    if df.empty:
        return pd.Series(dtype="object")

    df["year_num"] = df["year"].astype(str).str.extract(r"(\d+)$")[0]

    df = df.dropna(subset=["year_num"])

    if df.empty:
        return pd.Series(dtype="object")

    df["year_num"] = df["year_num"].astype(float).astype(int)

    df = df.sort_values("year_num")

    return df.iloc[-1]


# =====================================================
# Last 10 Years
# =====================================================


def last_10_years(df):

    if df.empty:
        return df

    df = df.copy()

    df = df.dropna(subset=["year"])

    if df.empty:
        return df

    df["year_num"] = df["year"].astype(str).str.extract(r"(\d+)$")[0]

    df = df.dropna(subset=["year_num"])

    if df.empty:
        return df

    df["year_num"] = df["year_num"].astype(float).astype(int)

    df = df.sort_values("year_num")

    return df.tail(10)


# =====================================================
# Header
# =====================================================


def draw_header(pdf, company):

    pdf.setFillColor(NAVY)

    pdf.rect(0, PAGE_HEIGHT - 0.80 * inch, PAGE_WIDTH, 0.80 * inch, fill=1, stroke=0)

    company_name = str(company["company_name"])

    ticker = str(company["company_id"] if "company_id" in company else company["id"])

    pdf.setFillColor(WHITE)

    pdf.setFont("Helvetica-Bold", 22)

    pdf.drawString(LEFT_MARGIN, PAGE_HEIGHT - 0.45 * inch, company_name)

    pdf.setFont("Helvetica", 11)

    pdf.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 0.45 * inch, ticker)


# =====================================================
# KPI Tile
# =====================================================


def draw_kpi_tile(pdf, x, y, width, height, title, value):

    pdf.setFillColor(LIGHT_GRAY)

    pdf.roundRect(x, y, width, height, 6, fill=1, stroke=0)

    pdf.setFillColor(NAVY)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawString(x + 8, y + height - 18, title)

    pdf.setFillColor(colors.black)

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawCentredString(x + width / 2, y + 18, str(value))


# =====================================================
# KPI Section
# =====================================================


def draw_kpi_section(pdf, company, ratios, cashflow):

    latest_ratio = latest_record(ratios)

    latest_cash = latest_record(cashflow)

    market_cap = "-"

    roe = latest_ratio.get("return_on_equity_pct", "-")

    roce = latest_ratio.get("return_on_capital_employed_pct", "-")

    pe = latest_ratio.get("pe", "-")

    debt = latest_ratio.get("debt_to_equity", "-")

    cfo = latest_cash.get("operating_activity", "-")

    start_x = LEFT_MARGIN

    start_y = PAGE_HEIGHT - 2.20 * inch

    gap_x = 0.20 * inch

    gap_y = 0.18 * inch

    tile_w = 2.15 * inch

    tile_h = 0.70 * inch

    tiles = [
        ("Market Cap", market_cap),
        ("ROE", roe),
        ("ROCE", roce),
        ("P/E", pe),
        ("Debt/Equity", debt),
        ("Operating CFO", cfo),
    ]

    index = 0

    for row in range(2):

        for col in range(3):

            x = start_x + col * (tile_w + gap_x)

            y = start_y - row * (tile_h + gap_y)

            title, value = tiles[index]

            draw_kpi_tile(pdf, x, y, tile_w, tile_h, title, value)

            index += 1


# =====================================================
# Revenue & Net Profit Charts
# =====================================================


def draw_financial_charts(pdf, profit_loss_df):

    df = last_10_years(profit_loss_df)

    if df.empty:
        return

    revenue = tuple(df["sales"].fillna(0))

    profit = tuple(df["net_profit"].fillna(0))

    years = list(df["year"])

    # ---------------- Revenue ----------------

    drawing = Drawing(250, 180)

    chart = VerticalBarChart()

    chart.x = 35
    chart.y = 30

    chart.width = 180
    chart.height = 120

    chart.data = [revenue]

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    drawing.add(chart)

    drawing.drawOn(pdf, LEFT_MARGIN, PAGE_HEIGHT - 6.30 * inch)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(
        LEFT_MARGIN + 110, PAGE_HEIGHT - 6.45 * inch, "10-Year Revenue"
    )

    # ---------------- Net Profit ----------------

    drawing = Drawing(250, 180)

    chart = VerticalBarChart()

    chart.x = 35
    chart.y = 30

    chart.width = 180
    chart.height = 120

    chart.data = [profit]

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    drawing.add(chart)

    drawing.drawOn(pdf, LEFT_MARGIN + 3.8 * inch, PAGE_HEIGHT - 6.30 * inch)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(
        LEFT_MARGIN + 3.8 * inch + 110, PAGE_HEIGHT - 6.45 * inch, "10-Year Net Profit"
    )


# =====================================================
# ROE & ROCE Chart
# =====================================================


def draw_ratio_chart(pdf, ratios_df):

    df = last_10_years(ratios_df)

    if df.empty:
        return

    years = list(df["year"].astype(str))

    roe = tuple(pd.to_numeric(df["return_on_equity_pct"], errors="coerce").fillna(0))

    roce = tuple(
        pd.to_numeric(df["return_on_capital_employed_pct"], errors="coerce").fillna(0)
    )

    drawing = Drawing(520, 180)

    chart = VerticalBarChart()

    chart.x = 45
    chart.y = 30

    chart.width = 420
    chart.height = 110

    chart.data = [roe, roce]

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = colors.darkblue
    chart.bars[1].fillColor = colors.darkgreen

    drawing.add(chart)

    drawing.drawOn(pdf, LEFT_MARGIN, PAGE_HEIGHT - 9.0 * inch)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(
        PAGE_WIDTH / 2, PAGE_HEIGHT - 9.15 * inch, "ROE vs ROCE (10 Years)"
    )


# =====================================================
# Balance Sheet Composition
# =====================================================


def draw_balance_sheet_chart(pdf, balance_df):

    df = last_10_years(balance_df)

    if df.empty:
        return

    years = list(df["year"])

    equity = tuple((df["equity_capital"] + df["reserves"]).fillna(0))

    borrowings = tuple(df["borrowings"].fillna(0))

    liabilities = tuple(df["other_liabilities"].fillna(0))

    drawing = Drawing(520, 220)

    chart = VerticalBarChart()

    chart.x = 45
    chart.y = 40

    chart.width = 380
    chart.height = 130

    chart.data = [equity, borrowings, liabilities]

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = colors.darkblue

    chart.bars[1].fillColor = colors.darkgreen

    chart.bars[2].fillColor = colors.orange

    drawing.add(chart)

    drawing.drawOn(pdf, LEFT_MARGIN, PAGE_HEIGHT - 3.80 * inch)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(
        PAGE_WIDTH / 2, PAGE_HEIGHT - 4.00 * inch, "Balance Sheet Composition"
    )


# =====================================================
# Cash Flow Waterfall
# =====================================================


def draw_cashflow_chart(pdf, cashflow_df):

    latest = latest_record(cashflow_df)

    if latest.empty:
        return

    values = [
        latest["operating_activity"],
        latest["investing_activity"],
        latest["financing_activity"],
        latest["net_cash_flow"],
    ]

    labels = ["CFO", "CFI", "CFF", "Net"]

    drawing = Drawing(320, 210)

    chart = VerticalBarChart()

    chart.x = 40
    chart.y = 35

    chart.width = 220
    chart.height = 120

    chart.data = [tuple(values)]

    chart.categoryAxis.categoryNames = labels

    drawing.add(chart)

    drawing.drawOn(pdf, PAGE_WIDTH - 4.0 * inch, PAGE_HEIGHT - 7.10 * inch)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(
        PAGE_WIDTH - 2.0 * inch, PAGE_HEIGHT - 7.25 * inch, "Cash Flow Summary"
    )


# =====================================================
# Word Wrap Paragraph
# =====================================================


def draw_wrapped_text(pdf, text, x, y, width, style):

    paragraph = Paragraph(text, style)

    w, h = paragraph.wrap(width, 500)

    paragraph.drawOn(pdf, x, y - h)

    return h


# =====================================================
# Pros Section
# =====================================================


def draw_pros_section(pdf, pros_cons_df):

    pdf.setFont("Helvetica-Bold", 12)

    pdf.setFillColor(GREEN)

    pdf.drawString(LEFT_MARGIN, 3.10 * inch, "Pros")

    y = 2.90 * inch

    pros = pros_cons_df["pros"].dropna().tolist()

    for text in pros:

        pdf.setFillColor(GREEN)

        pdf.circle(LEFT_MARGIN + 3, y + 4, 2, fill=1)

        pdf.setFillColor(colors.black)

        used = draw_wrapped_text(pdf, str(text), LEFT_MARGIN + 10, y, 250, SMALL_STYLE)

        y -= used + 6

        if y < 0.80 * inch:

            break


# =====================================================
# Cons Section
# =====================================================


def draw_cons_section(pdf, pros_cons_df):

    start_x = PAGE_WIDTH / 2 + 20

    pdf.setFont("Helvetica-Bold", 12)

    pdf.setFillColor(RED)

    pdf.drawString(start_x, 3.10 * inch, "Cons")

    y = 2.90 * inch

    cons = pros_cons_df["cons"].dropna().tolist()

    for text in cons:

        pdf.setFillColor(RED)

        pdf.circle(start_x + 3, y + 4, 2, fill=1)

        pdf.setFillColor(colors.black)

        used = draw_wrapped_text(pdf, str(text), start_x + 10, y, 230, SMALL_STYLE)

        y -= used + 6

        if y < 0.80 * inch:

            break


# =====================================================
# Capital Allocation Badge
# =====================================================


def draw_capital_badge(pdf, capital_df):

    latest = latest_record(capital_df)

    if latest.empty:

        label = "Not Available"

    else:

        label = str(latest.get("pattern_label", "Not Available"))[:25]

    x = PAGE_WIDTH - 2.60 * inch

    y = PAGE_HEIGHT - 0.90 * inch

    width = 1.90 * inch

    height = 0.45 * inch

    pdf.setFillColor(NAVY)

    pdf.roundRect(x, y, width, height, 8, fill=1, stroke=0)

    pdf.setFillColor(WHITE)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(x + width / 2, y + 15, label)

    pdf.setFont("Helvetica", 7)

    pdf.drawCentredString(x + width / 2, y + 4, "Capital Allocation")


# =====================================================
# Build Tearsheet
# =====================================================


def build_tearsheet(conn, company_id):

    logger.info("Generating Tearsheet : %s", company_id)

    company = load_company(conn, company_id)

    if company is None:

        logger.warning("%s not found.", company_id)

        return

    profit_loss = load_profit_loss(conn, company_id)

    balance_sheet = load_balance_sheet(conn, company_id)

    cashflow = load_cashflow(conn, company_id)

    ratios = load_financial_ratios(conn, company_id)

    pros_cons = load_pros_cons(conn, company_id)

    capital = load_capital_allocation(company_id)

    pdf, output_file = create_canvas(company_id)

    # =====================================================
    # PAGE 1
    # =====================================================

    draw_header(pdf, company)

    draw_kpi_section(pdf, company, ratios, cashflow)

    draw_financial_charts(pdf, profit_loss)

    draw_ratio_chart(pdf, ratios)

    pdf.showPage()

    # =====================================================
    # PAGE 2
    # =====================================================

    draw_header(pdf, company)

    draw_capital_badge(pdf, capital)

    draw_balance_sheet_chart(pdf, balance_sheet)

    draw_cashflow_chart(pdf, cashflow)

    draw_pros_section(pdf, pros_cons)

    draw_cons_section(pdf, pros_cons)

    pdf.save()

    logger.info("Saved : %s", output_file)


# =====================================================
# Test Companies
# =====================================================


def get_test_companies():

    return ["TCS", "HDFCBANK", "RELIANCE", "SUNPHARMA", "TATASTEEL"]


# =====================================================
# Main
# =====================================================


def main():

    logger.info("=" * 60)

    logger.info("Sprint 5 Day 33 Started")

    conn = None

    try:

        conn = connect_database()

        companies = get_test_companies()

        print("\n")

        print("=" * 60)

        print("Generating Company Tearsheets")

        print("=" * 60)

        for company in companies:

            print(f"Generating {company}...")

            build_tearsheet(conn, company)

        print("\n")

        print("=" * 60)

        print("Sprint 5 Day 33 Completed")

        print("=" * 60)

        print(f"Tearsheets Generated : {len(companies)}")

        print(f"Output Folder : {REPORT_DIR}")

        logger.info("Sprint 5 Day 33 Completed Successfully.")

    except Exception as e:
        import traceback

        print("\nERROR")
        print("-" * 60)
        traceback.print_exc()
        print("-" * 60)

    finally:

        if conn is not None:

            conn.close()


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    main()
