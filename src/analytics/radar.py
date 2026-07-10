"""
Sprint 3 - Day 19

Radar Charts
"""

import os
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DB_PATH = "db/nifty100.db"
OUTPUT_DIR = "reports/radar_charts"


def load_data():
    """
    Load financial ratios and peer groups
    """

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    peers = pd.read_sql(
        "SELECT company_id, peer_group_name FROM peer_groups",
        conn
    )

    conn.close()

    return ratios, peers


def prepare_master():
    """
    Merge ratios with peer groups
    """

    ratios, peers = load_data()

    master = ratios.merge(
        peers,
        on="company_id",
        how="left"
    )

    return master


def check_metrics(master):

    metrics = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]

    print("=" * 60)
    print("Checking Required Metrics")
    print("=" * 60)

    for metric in metrics:

        if metric in master.columns:
            print(f"✓ {metric}")
        else:
            print(f"✗ {metric} NOT FOUND")

    print()

    print("=" * 60)
    print("Radar Dataset")
    print("=" * 60)

    print("Rows :", len(master))
    print()

    print(master.head())

def normalize_metrics(data, metrics):
    """
    Normalize all metrics to 0-100 scale.
    Lower Debt/Equity gets higher score.
    """

    normalized = data.copy()

    for metric in metrics:

        minimum = normalized[metric].min()
        maximum = normalized[metric].max()

        if pd.isna(minimum) or pd.isna(maximum):
            normalized[metric] = 0

        elif maximum == minimum:
            normalized[metric] = 50

        else:
            normalized[metric] = (
                (normalized[metric] - minimum)
                / (maximum - minimum)
            ) * 100

    # Lower Debt/Equity is better
    normalized["debt_to_equity"] = (
        100 - normalized["debt_to_equity"]
    )

    return normalized


def create_radar_chart(
    company,
    peer_average,
    company_name,
    peer_group
):

    labels = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "Revenue CAGR",
        "Composite"
    ]

    company_values = company.tolist()
    peer_values = peer_average.tolist()

    company_values += company_values[:1]
    peer_values += peer_values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw={"polar": True}
    )

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company_name
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        linewidth=2,
        linestyle="--",
        label="Peer Average"
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    ax.set_ylim(0, 100)

    ax.set_title(
        f"{company_name}\n{peer_group}",
        fontsize=12
    )

    ax.legend(loc="upper right")

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    filename = os.path.join(
        OUTPUT_DIR,
        f"{company_name}_radar.png"
    )

    plt.savefig(
        filename,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

if __name__ == "__main__":

    master = prepare_master()

    print()

    check_metrics(master)

    print()
    print("=" * 60)
    print("Generating Radar Charts")
    print("=" * 60)

    # Latest record for each company
    latest = (
        master
        .sort_values("year")
        .groupby("company_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )

    metrics = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]

    # Normalize metrics
    normalized = normalize_metrics(
        latest,
        metrics
    )

    # Nifty100 average
    nifty_average = (
        normalized[metrics]
        .mean()
    )

    count = 0

    for _, row in normalized.iterrows():

        company_name = row["company_id"]

        peer_group = row["peer_group_name"]

        company_values = (
            row[metrics]
            .fillna(0)
        )

        # No peer group
        if pd.isna(peer_group):

            create_radar_chart(
                company_values,
                nifty_average,
                company_name,
                "Nifty 100 Average"
            )

            count += 1
            continue

        peer_data = normalized[
            normalized["peer_group_name"] == peer_group
        ]

        peer_average = (
            peer_data[metrics]
            .mean()
        )

        create_radar_chart(
            company_values,
            peer_average,
            company_name,
            peer_group
        )

        count += 1

    print()
    print("=" * 60)
    print("Radar Charts Summary")
    print("=" * 60)
    print(f"Charts Generated : {count}")
    print(f"Output Folder : {OUTPUT_DIR}")