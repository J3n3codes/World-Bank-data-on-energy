from pathlib import Path
import pandas as pd

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

INPUT_FILE = Path(
    "data/processed/world_bank_analysis_panel_with_regions.csv"
)

OUTPUT_DIR = Path("outputs/tables/regional_analysis")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

YEARLY_OUTPUT = OUTPUT_DIR / "regional_yearly_summary.csv"
OVERALL_OUTPUT = OUTPUT_DIR / "regional_overall_summary.csv"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

x_var = "electricity_access"
y_var = "life_expectancy"

print("Original panel rows:", len(df))

# --------------------------------------------------
# FILTER COUNTRY-LEVEL OBSERVATIONS
# --------------------------------------------------

country_df = df[
    df["country_code"].notna()
].copy()

print("Country-level rows:", len(country_df))

# Count country-level records without a region
missing_region = country_df["region"].isna().sum()

# Exclude aggregates and missing region classifications
country_df = country_df[
    country_df["region"].notna()
    & (country_df["region"] != "Aggregates")
].copy()

# Retain complete observations for both indicators
analysis_df = country_df.dropna(
    subset=[x_var, y_var]
).copy()

print("Country-level rows without region:", missing_region)
print("Complete observations:", len(analysis_df))


# --------------------------------------------------
# SUMMARY FUNCTION
# --------------------------------------------------

def calculate_summary(group):

    x = group[x_var]
    y = group[y_var]

    pearson = (
        x.corr(y, method="pearson")
        if x.nunique() > 1 and y.nunique() > 1
        else float("nan")
    )

    spearman = (
        x.corr(y, method="spearman")
        if x.nunique() > 1 and y.nunique() > 1
        else float("nan")
    )

    return {
        "observations": len(group),
        "unique_countries": group["country_code"].nunique(),
        "mean_electricity_access": x.mean(),
        "mean_life_expectancy": y.mean(),
        "pearson_correlation": pearson,
        "spearman_correlation": spearman,
    }


# --------------------------------------------------
# YEARLY REGIONAL ANALYSIS
# --------------------------------------------------

yearly_rows = []

for (region, year), group in analysis_df.groupby(
    ["region", "year"]
):
    row = {
        "region": region,
        "year": year,
    }
    row.update(calculate_summary(group))
    yearly_rows.append(row)

yearly_summary = pd.DataFrame(yearly_rows)

yearly_summary.to_csv(YEARLY_OUTPUT, index=False)


# --------------------------------------------------
# OVERALL REGIONAL ANALYSIS
# --------------------------------------------------

overall_rows = []

for region, group in analysis_df.groupby("region"):
    row = {"region": region}
    row.update(calculate_summary(group))
    overall_rows.append(row)

overall_summary = pd.DataFrame(overall_rows)

overall_summary.to_csv(OVERALL_OUTPUT, index=False)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\n" + "=" * 55)
print("REGIONAL ANALYSIS COMPLETE")
print("=" * 55)

print("\nYearly regional summary:")
print(yearly_summary.head(10).to_string(index=False))

print("\nOverall regional summary:")
print(overall_summary.to_string(index=False))

print("\nNumber of yearly regional groups:", len(yearly_summary))
print("Number of regions:", len(overall_summary))

print("\nSaved files:")
print(YEARLY_OUTPUT)
print(OVERALL_OUTPUT)
