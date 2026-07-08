"""
Sprint 3 - Day 17

Composite Quality Score
"""

import pandas as pd


def normalize(series, higher_is_better=True):
    """
    P10/P90 Winsorization + 0-100 scaling
    """

    s = series.fillna(0).astype(float)

    p10 = s.quantile(0.10)
    p90 = s.quantile(0.90)

    s = s.clip(lower=p10, upper=p90)

    if p90 == p10:
        return pd.Series(50, index=s.index)

    score = (s - p10) / (p90 - p10) * 100

    if not higher_is_better:
        score = 100 - score

    return score

def calculate_composite_score(df: pd.DataFrame):

    result = df.copy()

    # ---------- Profitability (35%) ----------
    roe = normalize(
        result["return_on_equity_pct"]
    )

    roce = normalize(
        result["return_on_capital_employed_pct"]
    )

    npm = normalize(
        result["net_profit_margin_pct"]
    )

    # ---------- Cash Quality (30%) ----------
    fcf = normalize(
        result["free_cash_flow_cr"]
    )

    cfo = normalize(
        result["cash_from_operations_cr"]
    )

    fcf_positive = (
        result["free_cash_flow_cr"] > 0
    ).astype(int) * 100

    # ---------- Growth (20%) ----------
    revenue = normalize(
        result["revenue_cagr_5yr"]
    )

    pat = normalize(
        result["pat_cagr_5yr"]
    )

    # ---------- Leverage (15%) ----------
    debt = normalize(
        result["debt_to_equity"],
        higher_is_better=False
    )

    icr = normalize(
        result["interest_coverage"]
    )

    result["composite_score"] = (

        roe * 0.15 +

        roce * 0.10 +

        npm * 0.10 +

        fcf * 0.15 +

        cfo * 0.10 +

        fcf_positive * 0.05 +

        revenue * 0.10 +

        pat * 0.10 +

        debt * 0.10 +

        icr * 0.05

    ).round(2)

    # ---------- Sector Relative Score ----------
    result["sector_relative_score"] = (
        result
        .groupby("broad_sector")["composite_score"]
        .transform(
            lambda x: (
                (
                    (x - x.min()) / 
                    (x.max() - x.min())
                ) * 100
            ).round(2)
            if x.max() != x.min() 
            else 100
        )
    )

    return result