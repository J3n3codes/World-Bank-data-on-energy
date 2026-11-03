
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

INPUT_FILE = Path(
    "data/processed/world_bank_panel.csv"
)

OUTPUT_FILE = Path(
    "data/processed/world_bank_analysis_panel.csv"
)

# --------------------------------------------------
# LOAD FULL PANEL
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Full panel shape:", df.shape)

# --------------------------------------------------
# SELECT CORE ANALYSIS INDICATORS
# --------------------------------------------------

analysis_columns = [
    "country_name",
    "country_code",
    "year",
    "population",
    "life_expectancy",
    "urban_population_percent",
    "gdp_per_capita",
    "drinking_water_access",
    "electricity_access",
    "mobile_subscriptions",
    "infant_mortality",
    "renewable_energy",
    "internet_users"
]

# Validate required columns
missing_columns = [
    col for col in analysis_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

analysis_df = df[analysis_columns].copy()

# --------------------------------------------------
# SAVE ANALYSIS PANEL
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

analysis_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# VALIDATION AND REPORT
# --------------------------------------------------

print("\nAnalysis panel shape:")
print(analysis_df.shape)

print("\nMissing values:")
print(analysis_df.isna().sum())

print("\nDuplicate country-year keys:")
print(
    analysis_df.duplicated(
        subset=["country_code", "year"]
    ).sum()
)

print(f"\nSaved: {OUTPUT_FILE}")
