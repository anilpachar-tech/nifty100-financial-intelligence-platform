import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "db" / "nifty100.db"

REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_DIR.mkdir(exist_ok=True)

OUTPUT_DIR.mkdir(exist_ok=True)


# ==========================================================
# Database Connection
# ==========================================================

def connect_database():
    """Return SQLite database connection."""

    return sqlite3.connect(DATABASE_PATH)


# ==========================================================
# Load Latest Financial Dataset
# ==========================================================

def load_dataset():

    conn = connect_database()

    query = """
    SELECT

        c.id AS company_id,
        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.revenue_cagr_5yr,
        fr.free_cash_flow_cr,
        fr.operating_profit_margin_pct

    FROM companies c

    LEFT JOIN sectors s

        ON c.id = s.company_id

    LEFT JOIN (
    
        SELECT *
        FROM financial_ratios f1


        WHERE rowid IN (
    
            SELECT rowid
            FROM financial_ratios f2

            WHERE company_id = f1.company_id

            ORDER BY year DESC

            LIMIT 1
        
        )

    ) fr

    ON c.id = fr.company_id


    ORDER BY c.id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ==========================================================
# Sector Median Imputation
# ==========================================================

def sector_imputation(df):

    feature_columns = [

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"

    ]

    for column in feature_columns:

        df[column] = (

            df.groupby("broad_sector")[column]

            .transform(

                lambda x: x.fillna(x.median())

            )

        )

    imputer = SimpleImputer(strategy="median")

    df[feature_columns] = imputer.fit_transform(

        df[feature_columns]

    )

    return df

# ==========================================================
# Feature Scaling
# ==========================================================

def prepare_features(df):
    """
    Scale clustering features using StandardScaler.
    """

    feature_columns = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"
    ]

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(df[feature_columns])

    return scaled_features, scaler


# ==========================================================
# Elbow Plot
# ==========================================================

def generate_elbow_plot(features):
    """
    Generate inertia plot for K = 2 to 10.
    """

    inertia = []

    k_values = range(2, 11)

    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(features)

        inertia.append(model.inertia_)

    plt.figure(figsize=(8, 5))

    plt.plot(
        k_values,
        inertia,
        marker="o",
        linewidth=2
    )

    plt.title("KMeans Elbow Curve")

    plt.xlabel("Number of Clusters (K)")

    plt.ylabel("Inertia")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(REPORT_DIR / "elbow_plot.png")

    plt.close()


# ==========================================================
# Run KMeans
# ==========================================================

def perform_clustering(features):
    """
    Perform KMeans clustering.
    """

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    cluster_ids = model.fit_predict(features)

    return model, cluster_ids


# ==========================================================
# Distance from Cluster Center
# ==========================================================

def calculate_distance(model, features):
    """
    Distance of every company from its assigned centroid.
    """

    distances = model.transform(features)

    nearest = distances.min(axis=1)

    return nearest

# ==========================================================
# Cluster Names
# ==========================================================

def assign_cluster_names(cluster_summary):
    """
    Assign descriptive names to clusters based on average ROE.
    """

    ordered = cluster_summary.sort_values(
        "return_on_equity_pct",
        ascending=False
    ).index.tolist()

    names = {
        ordered[0]: "High-Quality Compounders",
        ordered[1]: "Emerging Growth",
        ordered[2]: "Defensive Dividend Payers",
        ordered[3]: "Value Cyclicals",
        ordered[4]: "Distressed / Turnaround"
    }

    return names


# ==========================================================
# Save Cluster Labels
# ==========================================================

def save_cluster_labels(df, cluster_ids, distances):

    df["cluster_id"] = cluster_ids

    summary = (
        df.groupby("cluster_id")[
            "return_on_equity_pct"
        ]
        .mean()
        .to_frame()
    )

    cluster_names = assign_cluster_names(summary)

    df["cluster_name"] = df["cluster_id"].map(cluster_names)

    df["distance_from_centroid"] = distances.round(4)

    output = df[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid"
        ]
    ]

    output.to_csv(
        OUTPUT_DIR / "cluster_labels.csv",
        index=False
    )

    return output


# ==========================================================
# Validation
# ==========================================================

def validate_output(output_df):

    print("\n" + "=" * 55)
    print("KMeans Clustering Validation")
    print("=" * 55)

    print(f"Companies Clustered : {len(output_df)}")

    print(
        f"Unique Clusters     : {output_df['cluster_id'].nunique()}"
    )

    print("\nCluster Distribution\n")

    print(
        output_df["cluster_name"]
        .value_counts()
        .sort_index()
    )

    if len(output_df) == 92:
        print("\nPASS : All 92 companies clustered.")

    else:
        print("\nWARNING : Company count is not 92.")


# ==========================================================
# Main
# ==========================================================

def main():

    print("\nLoading financial data...")

    df = load_dataset()

    print(f"Companies Loaded : {len(df)}")

    print("\nPerforming sector-wise imputation...")

    df = sector_imputation(df)

    print("Scaling features...")

    features, scaler = prepare_features(df)

    print("Generating elbow plot...")

    generate_elbow_plot(features)

    print("Running KMeans clustering...")

    model, cluster_ids = perform_clustering(features)

    distances = calculate_distance(
        model,
        features
    )

    output = save_cluster_labels(
        df,
        cluster_ids,
        distances
    )

    validate_output(output)

    print("\nFiles Generated")

    print(f"  {REPORT_DIR / 'elbow_plot.png'}")
    print(f"  {OUTPUT_DIR / 'cluster_labels.csv'}")

    print("\nSprint 6 - Day 36 Completed")


if __name__ == "__main__":
    main()