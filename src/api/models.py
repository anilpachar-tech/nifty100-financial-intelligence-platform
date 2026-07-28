from typing import Optional

from pydantic import BaseModel

# ==========================================================
# Company Model
# ==========================================================


class Company(BaseModel):
    """Represents a company record."""

    id: str
    company_name: str


# ==========================================================
# Company Details Model
# ==========================================================


class CompanyDetails(BaseModel):
    """Represents detailed company information."""

    company_id: str
    company_name: str

    broad_sector: Optional[str] = None

    return_on_equity_pct: Optional[float] = None
    debt_to_equity: Optional[float] = None
    operating_profit_margin_pct: Optional[float] = None
    revenue_cagr_5yr: Optional[float] = None
    free_cash_flow_cr: Optional[float] = None
    composite_quality_score: Optional[float] = None

    cluster_name: Optional[str] = None


# ==========================================================
# Financial Model
# ==========================================================


class Financials(BaseModel):
    """Represents company financial metrics."""

    company_id: str
    year: str

    return_on_equity_pct: Optional[float] = None
    operating_profit_margin_pct: Optional[float] = None
    net_profit_margin_pct: Optional[float] = None

    debt_to_equity: Optional[float] = None
    interest_coverage: Optional[float] = None

    earnings_per_share: Optional[float] = None
    book_value_per_share: Optional[float] = None

    pe: Optional[float] = None
    pb: Optional[float] = None
    dividend_yield: Optional[float] = None

    composite_quality_score: Optional[float] = None


# ==========================================================
# Cluster Summary Model
# ==========================================================


class ClusterSummary(BaseModel):
    """Represents summary statistics for a cluster."""

    cluster_id: int
    cluster_name: str

    companies: int

    average_roe: float
    average_debt: float
    average_revenue_cagr: float
    average_fcf: float
    average_opm: float
