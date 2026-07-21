# 📊 Nifty100 Financial Intelligence Platform

A comprehensive Financial Intelligence Platform built using **Python, SQLite, Pandas, Plotly, and Streamlit** to analyze the financial performance of Nifty 100 companies.

The platform provides interactive dashboards, financial analytics, valuation analysis, stock screening, peer comparison, sector insights, and annual report management using a structured ETL pipeline.

---

# 🚀 Features

- ETL pipeline for financial datasets
- SQLite-based centralized database
- Data Quality validation
- Financial ratio analysis
- Valuation analytics
- Interactive Streamlit Dashboard
- Company Profile Analytics
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Analysis
- Annual Reports Browser
- CSV Export
- Cached database loading for faster performance

---

# 🛠️ Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Plotly
- Streamlit
- OpenPyXL
- Matplotlib

---

# 📂 Project Structure

```text
Nifty100-Financial-Intelligence-Platform
│
├── data/
├── db/
├── output/
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   └── utils/
│
├── tests/
├── assets/
├── README.md
└── requirements.txt
```

---

# ▶️ Running the Dashboard

## Clone Repository

```bash
git clone https://github.com/anilpachar-tech/nifty100-financial-intelligence-platform.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

# 📈 Dashboard Screens

## 1. Home

Provides an overview of the Financial Intelligence Platform including key statistics, navigation, and project summary.

![Home](assets/home.png)

---

## 2. Company Profile

Displays company financial information including Revenue, Profit, CAGR, financial ratios, and Pros & Cons.

![Company Profile](assets/company_profile.png)

---

## 3. Stock Screener

Allows filtering companies using valuation, profitability, leverage, and growth metrics with CSV export functionality.

![Stock Screener](assets/stock_screener.png)

---

## 4. Peer Comparison

Compares selected companies using important financial metrics and interactive charts.

![Peer Comparison](assets/peer_comparison.png)

---

## 5. Trend Analysis

Visualizes Revenue, Profit, EPS, Margins, and historical financial trends.

![Trend Analysis](assets/trend_analysis.png)

---

## 6. Sector Analysis

Provides sector-wise comparison, market capitalization insights, and financial statistics.

![Sector Analysis](assets/sector_analysis.png)

---

## 7. Capital Allocation

Analyzes ROE, ROCE, Debt, Cash Flow, and capital allocation efficiency.

![Capital Allocation](assets/capital_allocation.png)

---

## 8. Annual Reports

Browse and download company annual reports directly from the dashboard.

![Annual Reports](assets/annual_reports.png)

---

# 📦 Output Files

| File | Description |
|------|-------------|
| valuation_summary.xlsx | Valuation analysis for all companies |
| valuation_flags.csv | Discount and Caution flagged companies |
| load_audit.csv | ETL loading audit |
| nifty100.db | SQLite database |

---

# 🏁 Sprint Progress

## ✅ Sprint 1 — ETL Foundation

Completed:

- Project setup
- Folder structure
- SQLite database creation
- ETL pipeline
- Data loading
- Data validation
- Foreign key validation
- Duplicate detection
- Data Quality checks
- Load audit generation
- Unit testing

---

## ✅ Sprint 2 — Financial Analytics

Completed:

- Financial ratios
- CAGR calculations
- Growth analytics
- Profitability analysis
- Company-wise financial metrics
- Historical trend processing
- Analytics module development

---

## ✅ Sprint 3 — Dashboard Development

Completed:

- Streamlit multi-page dashboard
- Home page
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation dashboard
- Interactive Plotly visualizations
- Cached database loader

---

## ✅ Sprint 4 — Dashboard Enhancement & QA

Completed:

- Annual Reports dashboard
- Valuation analytics module
- FCF Yield calculation
- Median PE analysis
- Valuation flags
- Dashboard integration
- Performance optimization
- Integration testing
- Partial-data company testing
- CSV export validation
- Dashboard QA
- Documentation

---

# 📊 Sprint 4 Retrospective

## UX Decisions

- Implemented a clean multi-page Streamlit dashboard.
- Used cached database loading to improve responsiveness.
- Added interactive charts and filters.
- Maintained consistent UI across all pages.

### Data Edge Cases

- Tested companies with limited historical data.
- Verified dashboard stability with missing values.
- Validated extreme filter combinations.
- Confirmed valuation calculations for all companies.

### Performance Findings

- Company Profile loads within approximately 1–2 seconds.
- Dashboard remains responsive across all screens.
- CSV downloads generate valid output files.
- Valuation analytics successfully processed all 92 companies.

---

# 📌 Current Status

✅ Sprint 1 Completed

✅ Sprint 2 Completed

✅ Sprint 3 Completed

✅ Sprint 4 Completed

---

# 👨‍💻 Author

**Anil Pachar**

B.Tech Electrical Engineering

Financial Data Analytics Project

