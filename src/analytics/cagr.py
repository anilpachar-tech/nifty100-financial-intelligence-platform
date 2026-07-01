"""
Sprint 2 - Day 10

CAGR Engine
"""

from typing import Optional, Tuple


def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int
) -> Tuple[Optional[float], str]:
    """
    CAGR Formula

    Returns

    (
        CAGR,
        Flag
    )
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if years < 3:
        return None, "INSUFFICIENT"

    if start_value > 0 and end_value > 0:

        cagr = (
            (
                end_value /
                start_value
            ) ** (
                1 / years
            ) - 1
        ) * 100

        return round(
            cagr,
            2
        ), "NORMAL"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"

def revenue_cagr(
    start_sales: float,
    end_sales: float,
    years: int
) -> Tuple[Optional[float], str]:
    """
    Revenue CAGR
    """

    return calculate_cagr(
        start_sales,
        end_sales,
        years
    )


def pat_cagr(
    start_profit: float,
    end_profit: float,
    years: int
) -> Tuple[Optional[float], str]:
    """
    Profit After Tax CAGR
    """

    return calculate_cagr(
        start_profit,
        end_profit,
        years
    )


def eps_cagr(
    start_eps: float,
    end_eps: float,
    years: int
) -> Tuple[Optional[float], str]:
    """
    Earnings Per Share CAGR
    """

    return calculate_cagr(
        start_eps,
        end_eps,
        years
    )