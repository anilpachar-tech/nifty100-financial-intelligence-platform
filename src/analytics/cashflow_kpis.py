"""
Sprint 2 - Day 11

Cash Flow KPI Engine
"""

from typing import Optional


def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow

    Formula

    CFO + CFI

    Negative values
    are allowed.
    """

    return round(
        operating_activity +
        investing_activity,
        2
    )

def cfo_quality_score(
    average_cfo: float,
    average_pat: float
) -> tuple[Optional[float], Optional[str]]:
    """
    CFO Quality Score

    Formula

    Average CFO /
    Average PAT

    Returns

    (
        score,
        quality_label
    )
    """

    if average_pat == 0:
        return None, None

    score = round(
        average_cfo /
        average_pat,
        2
    )

    if score > 1.0:
        label = "High Quality"

    elif score >= 0.5:
        label = "Moderate"

    else:
        label = "Accrual Risk"

    return score, label

def capex_intensity(
    investing_activity: float,
    sales: float
) -> tuple[Optional[float], Optional[str]]:
    """
    CapEx Intensity

    Formula

    abs(CFI) / Sales * 100

    Returns

    (
        percentage,
        category
    )
    """

    if sales == 0:
        return None, None

    intensity = round(
        (
            abs(investing_activity) /
            sales
        ) * 100,
        2
    )

    if intensity < 3:
        category = "Asset Light"

    elif intensity <= 8:
        category = "Moderate"

    else:
        category = "Capital Intensive"

    return intensity, category

def fcf_conversion_rate(
    free_cash_flow: float,
    operating_profit: float
) -> tuple[Optional[float], Optional[str]]:
    """
    Free Cash Flow Conversion Rate

    Formula

    FCF / Operating Profit * 100

    Returns

    (
        conversion_rate,
        status
    )
    """

    if operating_profit == 0:
        return None, None

    conversion = round(
        (
            free_cash_flow /
            operating_profit
        ) * 100,
        2
    )

    if conversion >= 100:
        status = "Excellent"

    elif conversion >= 70:
        status = "Good"

    else:
        status = "Weak"

    return conversion, status

def capital_allocation_pattern(
    operating_activity: float,
    investing_activity: float,
    financing_activity: float,
    cfo_pat_ratio: Optional[float] = None
) -> str:
    """
    Capital Allocation Pattern Classifier

    Returns one of the predefined
    business pattern labels.
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    # (+,-,-)
    if cfo == "+" and cfi == "-" and cff == "-":

        if (
            cfo_pat_ratio is not None and
            cfo_pat_ratio > 1.0
        ):
            return "Shareholder Returns"

        return "Reinvestor"

    # (+,+,-)
    if cfo == "+" and cfi == "+" and cff == "-":
        return "Liquidating Assets"

    # (-,+,+)
    if cfo == "-" and cfi == "+" and cff == "+":
        return "Distress Signal"

    # (-,-,+)
    if cfo == "-" and cfi == "-" and cff == "+":
        return "Growth Funded by Debt"

    # (+,+,+)
    if cfo == "+" and cfi == "+" and cff == "+":
        return "Cash Accumulator"

    # (-,-,-)
    if cfo == "-" and cfi == "-" and cff == "-":
        return "Pre-Revenue"

    # (+,-,+)
    if cfo == "+" and cfi == "-" and cff == "+":
        return "Mixed"

    return "Other"