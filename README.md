# 📊 Nifty100 Financial Intelligence Platform

A comprehensive Financial Intelligence Platform built using **Python, SQLite, Pandas, Plotly, Streamlit, and FastAPI** to analyze the financial performance of Nifty 100 companies.

This project provides an end-to-end financial analytics solution, including ETL pipelines, data quality validation, financial ratio analysis, interactive dashboards, clustering analytics, PDF report generation, and REST APIs.

---

# 🚀 Key Features

### 📂 Data Engineering
- ETL pipeline for financial datasets
- SQLite centralized database
- Data Quality validation
- Duplicate detection
- Foreign key validation
- ETL audit reporting

### 📈 Financial Analytics
- Financial Ratio Analysis
- CAGR Analysis
- Growth Analytics
- Profitability Metrics
- Valuation Analytics
- Capital Allocation Analysis

### 📊 Interactive Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Dashboard
- Annual Reports Browser
- CSV Export
- Interactive Plotly Charts

### 📄 Report Generation
- Company PDF Tearsheets
- Sector Summary Reports
- Portfolio Summary Report

### 🤖 Machine Learning
- Company Clustering
- Cluster Profiling
- Sector Distribution Analysis

### 🌐 REST API
- FastAPI backend
- Swagger Documentation
- ReDoc Documentation
- Company APIs
- Financial APIs
- Cluster APIs
- Validation APIs

### ✅ Testing
- Pytest Unit Tests
- API Testing
- Data Validation
- Integration Testing

---

# 🛠 Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Plotly
- Streamlit
- FastAPI
- Pydantic
- Matplotlib
- OpenPyXL
- Pytest

---

# 📂 Project Structure

```text
Nifty100-Financial-Intelligence-Platform
│
├── assets/
│
├── data/
│
├── db/
│
├── output/
│
├── reports/
│
├── src/
│   ├── analytics/
│   ├── api/
│   ├── dashboard/
│   ├── etl/
│   └── utils/
│
├── tests/
│
├── README.md
├── requirements.txt
└── Makefile
```

---

# ▶️ Installation

## Clone Repository

```bash
git clone https://github.com/anilpachar-tech/nifty100-financial-intelligence-platform.git
```

Move into project directory

```bash
cd nifty100-financial-intelligence-platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py
```

Dashboard opens at

```
http://localhost:8501
```

---

# 🌐 Run REST API

```bash
uvicorn src.api.main:app --reload
```

API available at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

# 📡 REST API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home |
| GET | /health | Health Check |
| GET | /companies | List Companies |
| GET | /companies/{company_id} | Company Details |
| GET | /financials/{company_id} | Latest Financial Ratios |
| GET | /clusters | Company Clusters |
| GET | /clusters/summary | Cluster Summary |
| GET | /clusters/sectors | Cluster Sector Distribution |
| GET | /clusters/top-companies | Top Companies |
| GET | /validate | Validate Project Resources |
| GET | /info | Project Information |

---

# 📈 Dashboard Modules

## 🏠 Home

Project overview with summary statistics.

![Home](assets/home.png)

---

## 🏢 Company Profile

Displays revenue, profit, CAGR, ratios, valuation metrics, and company fundamentals.

![Company Profile](assets/company_profile.png)

---

## 📈 Stock Screener

Filter companies using valuation, profitability, leverage, and growth metrics.

![Stock Screener](assets/stock_screener.png)

---

## ⚖ Peer Comparison

Compare multiple companies using interactive charts.

![Peer Comparison](assets/peer_comparison.png)

---

## 📉 Trend Analysis

Historical Revenue, Profit, EPS, Margins, and Growth visualization.

![Trend Analysis](assets/trend_analysis.png)

---

## 🏭 Sector Analysis

Sector-wise comparison and financial insights.

![Sector Analysis](assets/sector_analysis.png)

---

## 💰 Capital Allocation

ROE, ROCE, Debt, Cash Flow, and Capital Efficiency.

![Capital Allocation](assets/capital_allocation.png)

---

## 📄 Annual Reports

Browse and download company annual reports.

![Annual Reports](assets/annual_reports.png)

---

# 📦 Generated Outputs

| File | Description |
|------|-------------|
| valuation_summary.xlsx | Company valuation summary |
| valuation_flags.csv | Discount and caution flags |
| load_audit.csv | ETL loading audit |
| cluster_labels.csv | Company cluster labels |
| cluster_summary.csv | Cluster statistics |
| cluster_sector_distribution.csv | Sector distribution |
| cluster_top_companies.csv | Top companies by cluster |
| portfolio_summary.pdf | Portfolio summary report |
| nifty100.db | SQLite database |

---

# 🏁 Sprint Progress

## ✅ Sprint 1 — ETL Foundation

Completed

- Project Setup
- Folder Structure
- SQLite Database
- ETL Pipeline
- Data Loading
- Data Validation
- Duplicate Detection
- Foreign Key Validation
- Load Audit
- Unit Testing

---

## ✅ Sprint 2 — Financial Analytics

Completed

- Financial Ratios
- CAGR Analysis
- Growth Analytics
- Profitability Analysis
- Historical Financial Processing
- Analytics Modules

---

## ✅ Sprint 3 — Dashboard Development

Completed

- Streamlit Multi-page Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Dashboard
- Interactive Plotly Charts
- Cached Database Loader

---

## ✅ Sprint 4 — Dashboard Enhancement

Completed

- Annual Reports Browser
- Valuation Analytics
- FCF Yield
- Median PE Analysis
- Dashboard Optimization
- Integration Testing
- CSV Export
- Documentation

---

## ✅ Sprint 5 — Advanced Analytics

Completed

- Company PDF Tearsheets
- Batch Report Generator
- Sector Reports
- Portfolio Summary
- K-Means Clustering
- Cluster Profiling

---

## ✅ Sprint 6 — API Development

Completed

- FastAPI REST API
- Swagger Documentation
- ReDoc Documentation
- Company Endpoints
- Financial Endpoints
- Cluster Endpoints
- Validation Endpoints
- Response Models
- Logging
- API Testing

---

# 📊 Project Statistics

- Companies Covered: **92**
- Financial Records: **5,000+**
- SQLite Database
- Interactive Dashboard
- REST API
- Automated Reports
- Machine Learning Analytics
- 37 Automated API Tests Passing

---

# 📌 Current Status

- ✅ Sprint 1 Completed
- ✅ Sprint 2 Completed
- ✅ Sprint 3 Completed
- ✅ Sprint 4 Completed
- ✅ Sprint 5 Completed
- ✅ Sprint 6 Completed

---

# 🚀 Future Enhancements

- Docker Deployment
- Authentication & Authorization
- Portfolio Tracking
- Live NSE/BSE Data Integration
- AI-based Stock Recommendation
- Cloud Deployment

---

# 👨‍💻 Author

**Anil Pachar**

B.Tech Electrical Engineering

Financial Intelligence Platform Project

---

# 📄 License

This project is developed for educational and internship purposes.