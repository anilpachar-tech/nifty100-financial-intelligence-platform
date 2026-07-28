from pathlib import Path
import os

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORTS_DIR = PROJECT_ROOT / "reports"


# ==========================================================
# API Configuration
# ==========================================================

API_TITLE = "Nifty100 Financial Intelligence API"

API_VERSION = "1.0.0"

API_DESCRIPTION = "REST API for company analytics, clustering and financial insights."


# ==========================================================
# Server Configuration
# ==========================================================

HOST = os.getenv("API_HOST", "127.0.0.1")

PORT = int(os.getenv("API_PORT", "8000"))

DEBUG = os.getenv("DEBUG", "True").lower() == "true"
