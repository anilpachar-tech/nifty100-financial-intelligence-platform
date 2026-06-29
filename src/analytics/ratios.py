"""
Sprint 2 - Day 08
Profitability Ratio Engine

Implements:
1. Net Profit Margin
2. Operating Profit Margin
3. Return on Equity (ROE)
4. Return on Capital Employed (ROCE)
5. Return on Assets (ROA)
"""

from typing import Optional


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """
    Net Profit Margin (%)

    Formula:
        (Net Profit / Sales) * 100

    Return None if sales is zero.
    """

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(
    operating_profit: float,
    sales: float
) -> Optional[float]:
    """
    Operating Profit Margin (%)

    Formula:
        (Operating Profit / Sales) * 100

    Return None if sales is zero.
    """

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def opm_cross_check(
    calculated_opm: float,
    source_opm: float
) -> bool:
    """
    Returns True if difference <= 1%
    Otherwise False.
    """

    if calculated_opm is None or source_opm is None:
        return False

    return abs(calculated_opm - source_opm) <= 1


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    ROE (%)

    Formula:
        Net Profit /
        (Equity Capital + Reserves)
        *100

    Return None if denominator <=0
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:
    """
    ROCE (%)

    Formula:
        EBIT /
        (Equity + Reserves + Borrowings)
        *100
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(
    net_profit: float,
    total_assets: float
) -> Optional[float]:
    """
    ROA (%)

    Formula:
        Net Profit /
        Total Assets
        *100
    """

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)


def is_financial_company(
    broad_sector: str
) -> bool:
    """
    Returns True for Financial companies.
    """

    if broad_sector is None:
        return False

    return broad_sector.strip().lower() == "financials"


def roce_benchmark(broad_sector: str) -> float:
    """
    Returns benchmark ROCE threshold.

    Financial companies use a lower sector-relative benchmark.
    Other sectors use the default benchmark.
    """

    if is_financial_company(broad_sector):
        return 8.0

    return 15.0