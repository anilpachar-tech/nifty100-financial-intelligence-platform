from pathlib import Path
import sqlite3

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from fastapi import Request
from fastapi.exceptions import RequestValidationError

from typing import List

from src.api.models import (
    Company,
    CompanyDetails,
    Financials,
    ClusterSummary
)


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

@app.get(
    "/companies",
    tags=["Companies"],
    summary="Get all companies",
    response_model=List[Company]
)
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

@app.get(
    "/companies/{company_id}",
    tags=["Companies"],
    summary="Get company details",
    response_model=CompanyDetails
)
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
# Latest Financial Ratios Endpoint
# ==========================================================

@app.get(
    "/financials/{company_id}",
    tags=["Financials"],
    summary="Get latest financial ratios",
    response_model=Financials
)
def get_financials(company_id: str):

    conn = get_connection()

    query = """
    SELECT

        company_id,
        year,

        return_on_equity_pct,
        operating_profit_margin_pct,
        net_profit_margin_pct,

        debt_to_equity,
        interest_coverage,

        earnings_per_share,
        book_value_per_share,

        pe,
        pb,
        dividend_yield,

        composite_quality_score

    FROM financial_ratios

    WHERE company_id = ?

    ORDER BY year DESC

    LIMIT 1
    """

    financials = pd.read_sql(
        query,
        conn,
        params=(company_id,)
    )

    conn.close()

    if financials.empty:

        return JSONResponse(
            status_code=404,
            content={
                "message": "Financial data not found."
            }
        )

    return financials.iloc[0].to_dict()

# ==========================================================
# Cluster Summary Endpoint
# ==========================================================

@app.get(
    "/clusters/summary",
    tags=["Analytics"],
    summary="Get cluster summary statistics",
    response_model=List[ClusterSummary]
)
def get_cluster_summary():

    summary_file = PROJECT_ROOT / "output" / "cluster_summary.csv"

    if not summary_file.exists():

        return JSONResponse(
            status_code=404,
            content={
                "message": "cluster_summary.csv not found."
            }
        )

    summary = pd.read_csv(summary_file)

    return summary.to_dict(orient="records")


# ==========================================================
# Sector Distribution Endpoint
# ==========================================================

@app.get(
    "/clusters/sectors",
    tags=["Analytics"],
    summary="Get sector distribution by cluster"
)
def get_cluster_sectors():

    sector_file = PROJECT_ROOT / "output" / "cluster_sector_distribution.csv"

    if not sector_file.exists():

        return JSONResponse(
            status_code=404,
            content={
                "message": "cluster_sector_distribution.csv not found."
            }
        )

    sectors = pd.read_csv(sector_file)

    return sectors.to_dict(orient="records")


# ==========================================================
# Top Companies Endpoint
# ==========================================================

@app.get(
    "/clusters/top-companies",
    tags=["Analytics"],
    summary="Get top companies from each cluster"
)
def get_top_companies():

    top_file = PROJECT_ROOT / "output" / "cluster_top_companies.csv"

    if not top_file.exists():

        return JSONResponse(
            status_code=404,
            content={
                "message": "cluster_top_companies.csv not found."
            }
        )

    top_companies = pd.read_csv(top_file)

    top_companies["company_name"] = (
        top_companies["company_name"]
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

    return top_companies.to_dict(orient="records")

# ==========================================================
# API Information Endpoint
# ==========================================================

@app.get(
    "/info",
    tags=["System"],
    summary="API information"
)
def api_info():

    return {
        "project": "Nifty100 Financial Intelligence Platform",
        "version": "1.0.0",
        "framework": "FastAPI",
        "database": "SQLite",
        "status": "Running",
        "available_endpoints": [
            "/",
            "/health",
            "/companies",
            "/companies/{company_id}",
            "/financials/{company_id}",
            "/clusters",
            "/clusters/summary",
            "/clusters/sectors",
            "/clusters/top-companies"
        ]
    }


# ==========================================================
# API Validation Endpoint
# ==========================================================

@app.get(
    "/validate",
    tags=["System"],
    summary="Validate API resources"
)
def validate_api():

    output_dir = PROJECT_ROOT / "output"

    validation = {
        "database_exists": DATABASE_PATH.exists(),
        "cluster_labels": (output_dir / "cluster_labels.csv").exists(),
        "cluster_summary": (output_dir / "cluster_summary.csv").exists(),
        "cluster_sector_distribution": (
            output_dir / "cluster_sector_distribution.csv"
        ).exists(),
        "cluster_top_companies": (
            output_dir / "cluster_top_companies.csv"
        ).exists()
    }

    return validation

# ==========================================================
# Global Exception Handler
# ==========================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc)
        }
    )


# ==========================================================
# Request Validation Handler
# ==========================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=422,
        content={
            "status": "validation_error",
            "errors": exc.errors()
        }
    )

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