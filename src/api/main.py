from pathlib import Path
import sqlite3

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "db" / "nifty100.db"


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="Nifty100 Financial Intelligence API",
    description="REST API for company analytics, clustering, financial ratios, and reports.",
    version="1.0.0"
)


# ==========================================================
# Database Connection
# ==========================================================

def get_connection():

    return sqlite3.connect(DATABASE_PATH)


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health", tags=["System"])
def health():

    try:

        conn = get_connection()

        conn.execute("SELECT 1")

        conn.close()

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as error:

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(error)
            }
        )


# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def home():

    return {
        "project": "Nifty100 Financial Intelligence Platform",
        "version": "1.0.0",
        "status": "API Running"
    }

# ==========================================================
# Companies List Endpoint
# ==========================================================

@app.get("/companies")
def get_companies():

    conn = get_connection()

    query = """
    SELECT
        id,
        company_name
    FROM companies
    ORDER BY company_name
    """

    companies = pd.read_sql(query, conn)

    conn.close()

    companies["company_name"] = (
    companies["company_name"]
    .str.replace("\n", " ", regex=False)
    .str.strip()
)

    return companies.to_dict(orient="records")

@app.get("/companies/{company_id}")
def get_company(company_id: str):

    conn = get_connection()

    query = """
    SELECT

        c.id AS company_id,
        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.operating_profit_margin_pct,
        fr.revenue_cagr_5yr,
        fr.free_cash_flow_cr,
        fr.composite_quality_score

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN (

        SELECT *
        FROM financial_ratios f1

        WHERE rowid IN (

            SELECT rowid
            FROM financial_ratios f2

            WHERE f2.company_id = f1.company_id

            ORDER BY year DESC

            LIMIT 1

        )

    ) fr

        ON c.id = fr.company_id

    WHERE c.id = ?
    """

    company = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    if company.empty:

        return JSONResponse(
            status_code=404,
            content={
                "message": "Company not found."
            }
        )

    cluster_file = PROJECT_ROOT / "output" / "cluster_labels.csv"

    if cluster_file.exists():

        clusters = pd.read_csv(cluster_file)

        company = company.merge(
            clusters[["company_id", "cluster_name"]],
            on="company_id",
            how="left"
        )

    return company.iloc[0].to_dict()

# ==========================================================
# Cluster Endpoint
# ==========================================================

@app.get("/clusters")
def get_clusters():

    cluster_file = PROJECT_ROOT / "output" / "cluster_labels.csv"

    if not cluster_file.exists():

        return JSONResponse(
            status_code=404,
            content={
                "message": "cluster_labels.csv not found."
            }
        )

    clusters = pd.read_csv(cluster_file)

    return clusters.to_dict(orient="records")


# ==========================================================
# Run API
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )