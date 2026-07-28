import sqlite3
from pathlib import Path

import pandas as pd

from tearsheet import connect_database, build_tearsheet

# =====================================================
# Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_DIR = OUTPUT_DIR / "tearsheets"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Load Companies
# =====================================================


def get_all_companies(conn):

    query = """
    SELECT id
    FROM companies
    ORDER BY id
    """

    df = pd.read_sql(query, conn)

    return df["id"].tolist()


# =====================================================
# Minimum Data Check
# =====================================================


def has_minimum_data(conn, company_id):

    query = """
    SELECT COUNT(DISTINCT year) AS years
    FROM profitandloss
    WHERE company_id=?
    """

    df = pd.read_sql(query, conn, params=[company_id])

    if df.empty:

        return False, 0

    years = int(df.iloc[0]["years"])

    return years >= 3, years


# =====================================================
# Batch Generation
# =====================================================


def generate_batch():

    conn = connect_database()

    companies = get_all_companies(conn)

    generated = 0

    skipped = []

    print("=" * 60)
    print("Batch Tearsheet Generation")
    print("=" * 60)

    for company in companies:

        ok, years = has_minimum_data(conn, company)

        if not ok:

            print(f"Skipping {company} ({years} years)")

            skipped.append({"company_id": company, "years_available": years})

            continue

        print(f"Generating {company}")

        build_tearsheet(conn, company)

        generated += 1

    conn.close()

    return generated, skipped


# =====================================================
# Save Skipped
# =====================================================


def save_skipped(skipped):

    if len(skipped) == 0:

        print()

        print("Skipped : 0")

        return

    skipped_df = pd.DataFrame(skipped)

    output_file = OUTPUT_DIR / "skipped_tearsheets.csv"

    skipped_df.to_csv(output_file, index=False)

    print()

    print(f"Skipped : {len(skipped)}")

    print(f"Saved : {output_file}")


def validate_tearsheets(expected_count):

    pdf_folder = Path("output/tearsheets")

    if not pdf_folder.exists():

        print("\nTearsheet folder not found.")

        return

    pdf_files = sorted(pdf_folder.glob("*_tearsheet.pdf"))

    print("\n" + "=" * 60)
    print("Tearsheet Validation")
    print("=" * 60)

    print(f"Expected PDFs : {expected_count}")
    print(f"Found PDFs    : {len(pdf_files)}")

    small_files = []

    for pdf in pdf_files:

        size_kb = pdf.stat().st_size / 1024

        if size_kb < 30:

            small_files.append((pdf.name, round(size_kb, 2)))

    if len(pdf_files) == expected_count:

        print("PDF Count     : PASS")

    else:

        print("PDF Count     : FAIL")

    if small_files:

        print(f"\nFiles smaller than 30 KB : {len(small_files)}")

        for name, size in small_files:

            print(f"  {name} -> {size} KB")

    else:

        print("Minimum Size  : PASS")


# =====================================================
# Main
# =====================================================


def main():

    generated, skipped = generate_batch()

    save_skipped(skipped)

    validate_tearsheets(generated)

    print()

    print("=" * 60)

    print("Batch Generation Completed")

    print("=" * 60)

    print(f"Generated : {generated}")


if __name__ == "__main__":

    main()
