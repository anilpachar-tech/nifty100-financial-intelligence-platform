import pandas as pd


def normalize_ticker(ticker):

    if pd.isna(ticker):
        return None

    return str(ticker).strip().upper()


def normalize_year(year):

    if pd.isna(year):
        return None

    year = str(year).strip()

    replacements = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }

    parts = year.replace("-", " ").split()

    if len(parts) == 2:

        month = replacements.get(parts[0][:3], "01")
        year_part = parts[1]

        if len(year_part) == 2:
            year_part = f"20{year_part}"

        return f"{year_part}-{month}"

    return year