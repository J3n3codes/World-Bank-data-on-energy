
from pathlib import Path
import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

TABLE_DIR = Path("outputs/tables")

PEARSON_FILE = TABLE_DIR / "pearson_correlation_matrix.csv"
SPEARMAN_FILE = TABLE_DIR / "spearman_correlation_matrix.csv"
SAMPLE_FILE = TABLE_DIR / "pairwise_sample_sizes.csv"

# --------------------------------------------------
# 2. Load correlation matrices and sample sizes
# --------------------------------------------------

pearson = pd.read_csv(PEARSON_FILE, index_col=0)
spearman = pd.read_csv(SPEARMAN_FILE, index_col=0)
sample_sizes = pd.read_csv(SAMPLE_FILE, index_col=0)

# --------------------------------------------------
# 3. Convert matrices into unique variable pairs
# --------------------------------------------------

def rank_correlations(correlation_matrix, sample_sizes, method):

    upper_triangle = np.triu(
        np.ones(correlation_matrix.shape),
        k=1
    ).astype(bool)

    results = correlation_matrix.where(
        upper_triangle
    ).stack().reset_index()

    results.columns = [
        "variable_1",
        "variable_2",
        "correlation"
    ]

    results["sample_size"] = [
        sample_sizes.loc[row.variable_1, row.variable_2]
        for row in results.itertuples()
    ]

    results["absolute_correlation"] = (
        results["correlation"].abs()
    )

    results["direction"] = np.where(
        results["correlation"] > 0,
        "Positive",
        "Negative"
    )

    results["sample_size_category"] = np.where(
        results["sample_size"] < 30,
        "Small sample (<30)",
        "Larger sample (>=30)"
    )

    results["method"] = method

    results = results.sort_values(
        "absolute_correlation",
        ascending=False
    )

    return results.reset_index(drop=True)


# --------------------------------------------------
# 4. Rank Pearson and Spearman correlations
# --------------------------------------------------

pearson_ranked = rank_correlations(
    pearson,
    sample_sizes,
    "Pearson"
)

spearman_ranked = rank_correlations(
    spearman,
    sample_sizes,
    "Spearman"
)

# --------------------------------------------------
# 5. Save separate and combined results
# --------------------------------------------------

pearson_ranked.to_csv(
    TABLE_DIR / "top_pearson_correlations.csv",
    index=False
)

spearman_ranked.to_csv(
    TABLE_DIR / "top_spearman_correlations.csv",
    index=False
)

combined = pd.concat(
    [pearson_ranked, spearman_ranked],
    ignore_index=True
)

combined.to_csv(
    TABLE_DIR / "top_bivariable_relationships.csv",
    index=False
)

# --------------------------------------------------
# 6. Print results
# --------------------------------------------------

print("\nTOP 20 PEARSON CORRELATIONS")
print(
    pearson_ranked.head(20).to_string(index=False)
)

print("\nTOP 20 SPEARMAN CORRELATIONS")
print(
    spearman_ranked.head(20).to_string(index=False)
)

print("\nSample-size categories:")
print(
    combined.groupby(
        ["method", "sample_size_category"]
    ).size()
)

print("\nBivariable ranking completed.")

print(f"\nSaved files in: {TABLE_DIR}")
