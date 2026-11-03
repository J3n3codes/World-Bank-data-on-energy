
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

INPUT_FILE = Path("data/processed/world_bank_panel.csv")
OUTPUT_DIR = Path("outputs/tables")
FIGURE_DIR = Path("outputs/figures/bivariable")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Read data
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

# Retain country-level observations only
df = df[df["country_code"].notna()].copy()

# --------------------------------------------------
# 3. Select all 15 indicators
# --------------------------------------------------

indicators = [
    "gdp_per_capita",
    "population",
    "electricity_access",
    "internet_users",
    "life_expectancy",
    "renewable_energy",
    "urban_population_percent",
    "infant_mortality",
    "mobile_subscriptions",
    "secondary_enrollment",
    "smoking_male",
    "smoking_female",
    "alcohol_consumption",
    "drinking_water_access",
    "diabetes_prevalence",
]

data = df[indicators]

# --------------------------------------------------
# 4. Calculate correlations and pairwise sample sizes
# --------------------------------------------------

pearson_corr = data.corr(method="pearson")
spearman_corr = data.corr(method="spearman")

sample_sizes = data.notna().astype(int).T.dot(
    data.notna().astype(int)
)

# --------------------------------------------------
# 5. Save correlation tables
# --------------------------------------------------

pearson_corr.to_csv(
    OUTPUT_DIR / "pearson_correlation_matrix.csv"
)

spearman_corr.to_csv(
    OUTPUT_DIR / "spearman_correlation_matrix.csv"
)

sample_sizes.to_csv(
    OUTPUT_DIR / "pairwise_sample_sizes.csv"
)

# --------------------------------------------------
# 6. Plot Pearson and Spearman heatmaps
# --------------------------------------------------

sns.set_theme(style="white")

for name, matrix in [
    ("Pearson", pearson_corr),
    ("Spearman", spearman_corr),
]:

    plt.figure(figsize=(15, 12))

    sns.heatmap(
        matrix,
        annot=True,
        fmt=".2f",
        cmap="Purples",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.5,
        cbar_kws={"label": "Correlation coefficient"},
    )

    plt.title(
        f"{name} Correlation Matrix — 15 World Bank Indicators",
        fontsize=15,
        pad=18,
    )

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / f"{name.lower()}_correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

# --------------------------------------------------
# 7. Print results
# --------------------------------------------------

print("\nBivariable correlation analysis completed.")

print(f"Country-level observations: {len(df)}")
print(f"Indicators analyzed: {len(indicators)}")

print("\nPearson correlation matrix:")
print(pearson_corr.round(3))

print("\nSpearman correlation matrix:")
print(spearman_corr.round(3))

print("\nPairwise sample sizes:")
print(sample_sizes)

print(f"\nTables saved in: {OUTPUT_DIR}")
print(f"Figures saved in: {FIGURE_DIR}")
