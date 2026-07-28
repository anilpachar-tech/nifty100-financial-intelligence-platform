from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


# ==========================================================
# Health API
# ==========================================================


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


# ==========================================================
# Home API
# ==========================================================


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "API Running"


# ==========================================================
# Companies API
# ==========================================================


def test_companies():

    response = client.get("/companies")

    assert response.status_code == 200

    companies = response.json()

    assert isinstance(companies, list)

    assert len(companies) > 0


# ==========================================================
# Company Details API
# ==========================================================


def test_company_details():

    response = client.get("/companies/TCS")

    assert response.status_code == 200

    company = response.json()

    assert company["company_id"] == "TCS"

    assert "company_name" in company

    assert "cluster_name" in company


# ==========================================================
# Financials API
# ==========================================================


def test_financials():

    response = client.get("/financials/TCS")

    assert response.status_code == 200

    financials = response.json()

    assert financials["company_id"] == "TCS"

    assert "return_on_equity_pct" in financials

    assert "year" in financials


# ==========================================================
# Cluster Summary API
# ==========================================================


def test_cluster_summary():

    response = client.get("/clusters/summary")

    assert response.status_code == 200

    summary = response.json()

    assert isinstance(summary, list)

    assert len(summary) == 5


# ==========================================================
# Cluster List API
# ==========================================================


def test_cluster_labels():

    response = client.get("/clusters")

    assert response.status_code == 200

    clusters = response.json()

    assert isinstance(clusters, list)

    assert len(clusters) == 92


# ==========================================================
# Invalid Company API
# ==========================================================


def test_invalid_company():

    response = client.get("/companies/INVALID_COMPANY")

    assert response.status_code == 404


# ==========================================================
# Invalid Financial API
# ==========================================================


def test_invalid_financials():

    response = client.get("/financials/INVALID_COMPANY")

    assert response.status_code == 404


# ==========================================================
# API Validation Endpoint
# ==========================================================


def test_validate():

    response = client.get("/validate")

    assert response.status_code == 200

    data = response.json()

    assert data["database_exists"] is True
    assert data["cluster_labels"] is True
    assert data["cluster_summary"] is True


# ==========================================================
# API Information Endpoint
# ==========================================================


def test_info():

    response = client.get("/info")

    assert response.status_code == 200

    info = response.json()

    assert info["project"] == "Nifty100 Financial Intelligence Platform"

    assert "available_endpoints" in info
