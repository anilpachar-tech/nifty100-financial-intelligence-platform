-- 1. Total companies in master table
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. Top 10 companies by latest sales
SELECT company_id, year, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- 3. Top 10 companies by latest net profit
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 4. Top 10 companies by total assets
SELECT company_id, year, total_assets
FROM balancesheet
ORDER BY total_assets DESC
LIMIT 10;

-- 5. Top 10 companies by net cash flow
SELECT company_id, year, net_cash_flow
FROM cashflow
ORDER BY net_cash_flow DESC
LIMIT 10;

-- 6. Average ROE by company
SELECT company_id, ROUND(AVG(return_on_equity_pct), 2) AS avg_roe
FROM financial_ratios
GROUP BY company_id
ORDER BY avg_roe DESC
LIMIT 10;

-- 7. Number of years available per company in profit and loss
SELECT company_id, COUNT(DISTINCT year) AS year_count
FROM profitandloss
GROUP BY company_id
ORDER BY year_count DESC;

-- 8. Companies with negative net profit
SELECT company_id, year, net_profit
FROM profitandloss
WHERE net_profit < 0
ORDER BY net_profit ASC;

-- 9. Sector-wise company count
SELECT broad_sector, COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

-- 10. Latest stock price snapshot
SELECT company_id, date, close_price, adjusted_close
FROM stock_prices
ORDER BY date DESC
LIMIT 20;