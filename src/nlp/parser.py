"""
Sprint 5 - Day 29
NLP Analysis Parser

Reads analysis.xlsx and converts text-based financial metrics
into structured data using regular expressions.

"""

from pathlib import Path
import logging
import re
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "output"

ANALYSIS_FILE = RAW_DATA_DIR / "analysis.xlsx"

OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================================
# Logging Configuration
# ==========================================================

logging.basicConfig(
    filename=OUTPUT_DIR / "parser.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# Expected Columns
# ==========================================================

REQUIRED_COLUMNS = [
    "id",
    "company_id",
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

# ==========================================================
# Regex Pattern
# ==========================================================

PATTERN = re.compile(
    r"(TTM|Last\s*Year|\d+\s*Years?|\d+\s*Year)\s*:?\s*(-?\d+(?:\.\d+)?)%",
    re.IGNORECASE
)

# ==========================================================
# Load Dataset
# ==========================================================

def load_analysis_data() -> pd.DataFrame:
    """
    Load analysis.xlsx

    Returns
    -------
    pd.DataFrame
    """

    logger.info("Loading analysis.xlsx")

    if not ANALYSIS_FILE.exists():
        raise FileNotFoundError(
            f"Analysis file not found:\n{ANALYSIS_FILE}"
        )

    df = pd.read_excel(
        ANALYSIS_FILE,
        header=1
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    logger.info(
        "Loaded %d rows and %d columns",
        len(df),
        len(df.columns)
    )

    return df

# ==========================================================
# Validate Columns
# ==========================================================

def validate_columns(df: pd.DataFrame):

    missing = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    logger.info("Column validation successful.")

# ==========================================================
# Parse Single Text Cell
# ==========================================================

def parse_text(text):

    """
    Example

    Input

    10 Years: 21%
    5 Years: 18%
    TTM: -3%

    Output

    {
        "10 Years":21,
        "5 Years":18,
        "TTM":-3
    }
    """

    if pd.isna(text):
        return {}

    text = str(text).strip()

    matches = PATTERN.findall(text)

    parsed = {}

    for label, value in matches:

        label = (
            label
            .replace("Year", "Years")
            .replace("Yearss", "Years")
            .strip()
            .title()
        )

        try:
            parsed[label] = float(value)
        except ValueError:
            continue

    return parsed

# ==========================================================
# Parse Complete DataFrame
# ==========================================================

def parse_dataframe(df):

    target_columns = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]

    company_data = {}

    failed_rows = []

    logger.info("Parsing analysis text fields...")

    for _, row in df.iterrows():

        company_id = row["company_id"]

        if company_id not in company_data:
            company_data[company_id] = {
                "company_id": company_id
            }

        success = False

        for column in target_columns:

            parsed = parse_text(row[column])

            if parsed:
                success = True

            for key, value in parsed.items():

                clean_key = (
                    key.lower()
                    .replace(" ", "_")
                )

                company_data[company_id][
                    f"{column}_{clean_key}"
                ] = value

        if not success:
            failed_rows.append({
                "id": row["id"],
                "company_id": company_id
            })

    parsed_df = pd.DataFrame(
        company_data.values()
    )

    logger.info(
        "Companies Parsed : %d",
        len(parsed_df)
    )

    logger.info(
        "Failed Records : %d",
        len(failed_rows)
    )

    return (
        parsed_df,
        pd.DataFrame(failed_rows)
    )

# ==========================================================
# Save Output Files
# ==========================================================

def save_outputs(parsed_df, failed_df):
    """
    Save parsed and failed records to CSV files.
    """

    parsed_file = OUTPUT_DIR / "analysis_parsed.csv"
    failed_file = OUTPUT_DIR / "parse_failures.csv"

    parsed_df.to_csv(parsed_file, index=False)

    failed_df.to_csv(failed_file, index=False)

    logger.info("Saved parsed output : %s", parsed_file)
    logger.info("Saved failed output : %s", failed_file)

    return parsed_file, failed_file


# ==========================================================
# Print Summary
# ==========================================================

def print_summary(df, parsed_df, failed_df):

    print("\n" + "=" * 60)
    print("Sprint 5 - Day 29")
    print("NLP Analysis Parser Summary")
    print("=" * 60)

    print(f"Input Records      : {len(df)}")
    print(f"Companies Parsed   : {len(parsed_df)}")
    print(f"Failed Records     : {len(failed_df)}")

    failed = len(failed_df)

    success_rate = (
        ((len(df) - failed) / len(df)) * 100
        if len(df) > 0 else 0
    )

    print(f"Success Rate       : {success_rate:.2f}%")

    print("\nGenerated Files")
    print("-" * 60)
    print(f"{OUTPUT_DIR / 'analysis_parsed.csv'}")
    print(f"{OUTPUT_DIR / 'parse_failures.csv'}")
    print(f"{OUTPUT_DIR / 'parser.log'}")

    print("=" * 60)


# ==========================================================
# Main Function
# ==========================================================

def main():

    logger.info("=" * 60)
    logger.info("Sprint 5 Day 29 Parser Started")
    logger.info("=" * 60)

    try:

        # Load Dataset
        df = load_analysis_data()

        # Validate Columns
        validate_columns(df)

        # Parse Dataset
        parsed_df, failed_df = parse_dataframe(df)

        # Save Outputs
        save_outputs(
            parsed_df,
            failed_df
        )

        # Print Summary
        print_summary(
            df,
            parsed_df,
            failed_df
        )

        logger.info("Parser completed successfully.")

    except Exception as e:

        logger.exception("Parser Failed")

        print("\nERROR")
        print("-" * 50)
        print(e)
        print("-" * 50)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()