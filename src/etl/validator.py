import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")
OUTPUT_PATH = Path("output")

validation_errors = []


def log_error(file_name, rule_id, message):

    validation_errors.append(
        {
            "file_name": file_name,
            "rule_id": rule_id,
            "message": message
        }
    )


def validate_companies():

    df = pd.read_excel(RAW_PATH / "companies.xlsx", header=1)

    print(f"Companies Records : {len(df)}")

    if df["id"].isnull().sum() > 0:
        log_error("companies.xlsx", "DQ-01", "Null company ids found")
    print("DQ-01 Checked")

    if df["id"].duplicated().sum() > 0:
        log_error("companies.xlsx", "DQ-02", "Duplicate company ids found")
    print("DQ-02 Checked")

    if df["company_name"].isnull().sum() > 0:
        log_error("companies.xlsx", "DQ-03", "Missing company names found")
    print("DQ-03 Checked")

    if df["website"].isnull().sum() > 0:
        log_error("companies.xlsx", "DQ-04", "Missing website values found")
    print("DQ-04 Checked")


def validate_profitandloss():

    df = pd.read_excel(RAW_PATH / "profitandloss.xlsx", header=1)

    print(f"Profit & Loss Records : {len(df)}")

    invalid_sales = (df["sales"] <= 0).sum()

    if invalid_sales > 0:
        log_error(
            "profitandloss.xlsx",
            "DQ-05",
            f"{invalid_sales} rows have non-positive sales"
        )
    print("DQ-05 Checked")

    null_opm = df["opm_percentage"].isnull().sum()

    if null_opm > 0:
        log_error(
            "profitandloss.xlsx",
            "DQ-06",
            f"{null_opm} rows have missing OPM percentage"
        )
    print("DQ-06 Checked")


def validate_balancesheet():

    df = pd.read_excel(RAW_PATH / "balancesheet.xlsx", header=1)

    print(f"Balance Sheet Records : {len(df)}")

    invalid_assets = (df["total_assets"] <= 0).sum()

    if invalid_assets > 0:
        log_error(
            "balancesheet.xlsx",
            "DQ-07",
            f"{invalid_assets} rows have non-positive total assets"
        )
    print("DQ-07 Checked")

    invalid_liabilities = (df["total_liabilities"] <= 0).sum()

    if invalid_liabilities > 0:
        log_error(
            "balancesheet.xlsx",
            "DQ-08",
            f"{invalid_liabilities} rows have non-positive total liabilities"
        )
    print("DQ-08 Checked")


def validate_cashflow():

    df = pd.read_excel(RAW_PATH / "cashflow.xlsx", header=1)

    print(f"Cash Flow Records : {len(df)}")

    null_cashflow = df["net_cash_flow"].isnull().sum()

    if null_cashflow > 0:
        log_error(
            "cashflow.xlsx",
            "DQ-09",
            f"{null_cashflow} rows have missing net cash flow"
        )
    print("DQ-09 Checked")

    null_company_id = df["company_id"].isnull().sum()

    if null_company_id > 0:
        log_error(
            "cashflow.xlsx",
            "DQ-10",
            f"{null_company_id} rows have missing company id"
        )
    print("DQ-10 Checked")


def validate_analysis():

    df = pd.read_excel(RAW_PATH / "analysis.xlsx", header=1)

    print(f"Analysis Records : {len(df)}")

    if df["roe"].isnull().sum() > 0:
        log_error(
            "analysis.xlsx",
            "DQ-11",
            "Missing ROE values found"
        )
    print("DQ-11 Checked")

    if df["stock_price_cagr"].isnull().sum() > 0:
        log_error(
            "analysis.xlsx",
            "DQ-12",
            "Missing Stock Price CAGR values found"
        )
    print("DQ-12 Checked")


def validate_documents():

    df = pd.read_excel(RAW_PATH / "documents.xlsx", header=1)

    print(f"Documents Records : {len(df)}")

    if df["Annual_Report"].isnull().sum() > 0:
        log_error(
            "documents.xlsx",
            "DQ-13",
            "Missing Annual Report values found"
        )
    print("DQ-13 Checked")

    if df["company_id"].isnull().sum() > 0:
        log_error(
            "documents.xlsx",
            "DQ-14",
            "Missing company id values found"
        )
    print("DQ-14 Checked")


def validate_prosandcons():

    df = pd.read_excel(RAW_PATH / "prosandcons.xlsx", header=1)

    print(f"Pros & Cons Records : {len(df)}")

    if df["pros"].isnull().sum() > 0:
        log_error(
            "prosandcons.xlsx",
            "DQ-15",
            "Missing pros values found"
        )
    print("DQ-15 Checked")


def validate_sectors():

    df = pd.read_excel(
        RAW_PATH / "supporting datasets" / "sectors.xlsx"
    )

    print(f"Sectors Records : {len(df)}")

    if df["broad_sector"].isnull().sum() > 0:
        log_error(
            "sectors.xlsx",
            "DQ-16",
            "Missing broad sector values found"
        )
    print("DQ-16 Checked")


def generate_report():

    OUTPUT_PATH.mkdir(exist_ok=True)

    report = pd.DataFrame(validation_errors)

    report.to_csv(
        OUTPUT_PATH / "validation_failures.csv",
        index=False
    )

    print("\nValidation Report Generated")


if __name__ == "__main__":

    validate_companies()
    validate_profitandloss()
    validate_balancesheet()
    validate_cashflow()
    validate_analysis()
    validate_documents()
    validate_prosandcons()
    validate_sectors()

    generate_report()