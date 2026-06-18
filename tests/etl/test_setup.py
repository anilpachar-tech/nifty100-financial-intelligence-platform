from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.etl.normaliser import normalize_ticker
from src.etl.normaliser import normalize_year


print(normalize_ticker(" tcs "))
print(normalize_ticker("hdfcbank"))

print(normalize_year("Mar-23"))
print(normalize_year("Dec 2012"))