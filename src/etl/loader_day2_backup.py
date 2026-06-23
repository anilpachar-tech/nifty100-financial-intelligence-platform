from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw")

CORE_FILES = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

SUPPLEMENTARY_FILES = [
    "sectors.xlsx",
    "stock_prices.xlsx",
    "market_cap.xlsx",
    "financial_ratios.xlsx",
    "peer_groups.xlsx"
]


def load_core_files():

    results = []

    for file in CORE_FILES:

        try:

            file_path = RAW_PATH / file

            df = pd.read_excel(
                file_path,
                header=1
            )

            results.append(
                {
                    "file_name": file,
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "status": "SUCCESS"
                }
            )

            print(f"Loaded {file}")

        except Exception as e:

            results.append(
                {
                    "file_name": file,
                    "rows": 0,
                    "columns": 0,
                    "status": f"FAILED : {e}"
                }
            )

    return results


def load_supporting_files():

    results = []

    supporting_path = RAW_PATH / "supporting datasets"

    for file in SUPPLEMENTARY_FILES:

        try:

            file_path = supporting_path / file

            df = pd.read_excel(file_path)

            results.append(
                {
                    "file_name": file,
                    "rows": df.shape[0],
                    "columns": df.shape[1],
                    "status": "SUCCESS"
                }
            )

            print(f"Loaded {file}")

        except Exception as e:

            results.append(
                {
                    "file_name": file,
                    "rows": 0,
                    "columns": 0,
                    "status": f"FAILED : {e}"
                }
            )

    return results


if __name__ == "__main__":

    core = load_core_files()
    supporting = load_supporting_files()

    audit = pd.DataFrame(core + supporting)

    Path("output").mkdir(exist_ok=True)

    audit.to_csv(
        "output/load_audit.csv",
        index=False
    )

    print("\nLoad Audit Generated")