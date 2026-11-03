from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

INPUT_FILE = Path(
    "data/processed/world_bank_analysis_panel.csv"
)

OUTPUT_TABLES = Path("outputs/tables")
OUTPUT_FIGURES = Path("outputs/figures")

YEARLY_FIGURES = OUTPUT_FIGURES / "gdp_electricity_yearly"

OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
OUTPUT_FIGURES.mkdir(parents=True, exist_ok=True)
YEARLY_FIGURES.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load and prepare data
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

# Retain country-level observations only
df = df[df["country_code"].notna()].copy()

# Retain observations where both variables are available
paired = df.dropna(
    subset=["gdp_per_capita", "electricity_access"]
).copy()

print("=" * 65)
print("GDP PER CAPITA VS ELECTRICITY ACCESS")
print("=" * 65)

print("Country-level rows:", len(df))
print("Paired observations:", len(paired))
print("Year range:", paired["year"].min(), "-", paired["year"].max())


# --------------------------------------------------
# 3. Pooled correlation
# --------------------------------------------------

pooled_correlation = paired[
    "gdp_per_capita"
].corr(paired["electricity_access"])

pooled_summary = pd.DataFrame([{
    "analysis": "GDP per capita vs electricity access",
    "observations": len(paired),
    "pearson_correlation": pooled_correlation,
    "first_year": paired["year"].min(),
    "last_year": paired["year"].max()
}])

pooled_summary.to_csv(
    OUTPUT_TABLES / "gdp_electricity_pooled_summary.csv",
    index=False
)

print("\nPooled Pearson correlation:", round(pooled_correlation, 4))


# --------------------------------------------------
# 4. Pooled scatter plot
# --------------------------------------------------

# --------------------------------------------------
# 4. Pooled scatter plot
# --------------------------------------------------

plt.figure(figsize=(10, 7))

plt.scatter(
    paired["electricity_access"],
    paired["gdp_per_capita"],
    alpha=0.35
)

plt.xlabel("Electricity access (% of population)")
plt.ylabel("GDP per capita (current US$)")
plt.title(
    "Electricity Access vs GDP per Capita\n"
    "Pooled Country-Year Observations, 2000–2023"
)

plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    OUTPUT_FIGURES / "gdp_per_capita_vs_electricity_access.png",
    dpi=300
)

plt.close()



# --------------------------------------------------
# 5. Yearly correlations
# --------------------------------------------------

yearly_results = []

for year, group in paired.groupby("year"):

    n = len(group)

    correlation = (
        group["gdp_per_capita"].corr(
            group["electricity_access"]
        )
        if n >= 2 else float("nan")
    )

    yearly_results.append({
        "year": year,
        "observations": n,
        "pearson_correlation": correlation
    })

yearly_correlations = pd.DataFrame(yearly_results)

yearly_correlations.to_csv(
    OUTPUT_TABLES / "gdp_electricity_yearly_correlations.csv",
    index=False
)

print("\nYEARLY CORRELATIONS")
print(yearly_correlations.round(4).to_string(index=False))


# --------------------------------------------------
# 6. Yearly scatter-plot grid
# --------------------------------------------------

years = sorted(paired["year"].unique())

ncols = 4
nrows = (len(years) + ncols - 1) // ncols

fig, axes = plt.subplots(
    nrows,
    ncols,
    figsize=(18, nrows * 4),
    squeeze=False
)

axes = axes.flatten()

for ax, year in zip(axes, years):

    group = paired[paired["year"] == year]

    r = group["gdp_per_capita"].corr(
        group["electricity_access"]
    )

    ax.scatter(
        group["electricity_access"],
        group["gdp_per_capita"],
        alpha=0.5
    )

    ax.set_title(
        f"{year} | n={len(group)} | r={r:.2f}"
    )

    ax.set_xlabel("Electricity access (%)")
    ax.set_ylabel("GDP per capita (US$)")
    ax.grid(alpha=0.2)

# Hide unused panels
for ax in axes[len(years):]:
    ax.set_visible(False)

fig.suptitle(
    "GDP per Capita vs Electricity Access by Year",
    fontsize=16,
    y=1.01
)

plt.tight_layout()

plt.savefig(
    OUTPUT_FIGURES / "gdp_electricity_yearly_grid.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    OUTPUT_FIGURES / "gdp_electricity_yearly_grid.pdf",
    bbox_inches="tight"
)

plt.close()


# --------------------------------------------------
# 7. Completion message
# --------------------------------------------------

print("\n" + "=" * 65)
print("ANALYSIS COMPLETE")
print("=" * 65)

print("\nGenerated files:")
print(OUTPUT_TABLES / "gdp_electricity_pooled_summary.csv")
print(OUTPUT_TABLES / "gdp_electricity_yearly_correlations.csv")
print(OUTPUT_FIGURES / "gdp_per_capita_vs_electricity_access.png")
print(OUTPUT_FIGURES / "gdp_electricity_yearly_grid.png")
print(OUTPUT_FIGURES / "gdp_electricity_yearly_grid.pdf")
