"""
Sprint 2 - Day 08 & Day 09
Financial Ratio Engine

Implements:
1. Net Profit Margin
2. Operating Profit Margin
3. OPM Cross Check
4. Return on Equity (ROE)
5. Return on Capital Employed (ROCE)
6. Return on Assets (ROA)
7. Debt to Equity
8. High Leverage Flag
9. Interest Coverage Ratio
10. ICR Label
11. ICR Warning Flag
12. Net Debt
13. Asset Turnover
"""

from typing import Optional


def net_profit_margin(
    net_profit: float,
    sales: float
) -> Optional[float]:
    """
    Net Profit Margin (%)

    Formula:
    (Net Profit / Sales) * 100

    Return None if sales is zero.
    """

    if sales == 0:
        return None

    return round(
        (net_profit / sales) * 100,
        2
    )


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

    return round(
        (operating_profit / sales) * 100,
        2
    )


def opm_cross_check(
    calculated_opm: float,
    source_opm: float
) -> bool:
    """
    Returns True when
    difference <= 1%
    """

    if calculated_opm is None:
        return False

    if source_opm is None:
        return False

    return abs(
        calculated_opm -
        source_opm
    ) <= 1


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    Return on Equity (ROE)
    """

    equity = (
        equity_capital +
        reserves
    )

    if equity <= 0:
        return None

    return round(
        (net_profit / equity) * 100,
        2
    )


def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:
    """
    Return on Capital Employed (ROCE)
    """

    capital = (
        equity_capital +
        reserves +
        borrowings
    )

    if capital <= 0:
        return None

    return round(
        (ebit / capital) * 100,
        2
    )


def return_on_assets(
    net_profit: float,
    total_assets: float
) -> Optional[float]:
    """
    Return on Assets
    """

    if total_assets == 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2
    )


def is_financial_company(
    broad_sector: str
) -> bool:
    """
    Returns True
    for Financial companies.
    """

    if broad_sector is None:
        return False

    return (
        broad_sector
        .strip()
        .lower()
        == "financials"
    )


def roce_benchmark(
    broad_sector: str
) -> float:
    """
    ROCE benchmark.
    """

    if is_financial_company(
        broad_sector
    ):
        return 8.0

    return 15.0


def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    Debt to Equity Ratio
    """

    if borrowings == 0:
        return 0.0

    equity = (
        equity_capital +
        reserves
    )

    if equity <= 0:
        return None

    return round(
        borrowings / equity,
        2
    )

def high_leverage_flag(
    debt_equity: Optional[float],
    broad_sector: str
) -> bool:
    """
    Returns True if Debt-to-Equity
    is greater than 5.

    Financial companies
    are excluded.
    """

    if debt_equity is None:
        return False

    if is_financial_company(
        broad_sector
    ):
        return False

    return debt_equity > 5


def interest_coverage_ratio(
    operating_profit: float,
    other_income: float,
    interest: float
) -> Optional[float]:
    """
    Interest Coverage Ratio

    Formula:
    (Operating Profit + Other Income)
    / Interest

    Return None if interest is zero.
    """

    if interest == 0:
        return None

    return round(
        (
            operating_profit +
            other_income
        ) / interest,
        2
    )


def icr_label(
    interest: float
) -> str:
    """
    Display label for
    debt-free companies.
    """

    if interest == 0:
        return "Debt Free"

    return ""


def icr_warning_flag(
    icr: Optional[float]
) -> bool:
    """
    Returns True if
    Interest Coverage Ratio
    is below 1.5
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings: float,
    investments: float
) -> float:
    """
    Net Debt

    Borrowings - Investments
    """

    return round(
        borrowings -
        investments,
        2
    )


def asset_turnover(
    sales: float,
    total_assets: float
) -> Optional[float]:
    """
    Asset Turnover

    Formula:
    Sales / Total Assets

    Return None if
    total assets are zero.
    """

    if total_assets == 0:
        return None

    return round(
        sales /
        total_assets,
        2
    )