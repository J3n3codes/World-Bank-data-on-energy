from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/world_bank_analysis_panel.csv")
OUTPUT_FILE = Path("outputs/tables/correlation_matrix.csv")

df = pd.read_csv(INPUT_FILE)

numeric_columns = [
    "population",
    "life_expectancy",
    "urban_population_percent",
    "gdp_per_capita",
    "drinking_water_access",
    "electricity_access",
    "mobile_subscriptions",
    "infant_mortality",
    "renewable_energy",
    "internet_users",
]

corr_matrix = df[numeric_columns].corr()

corr_matrix.to_csv(OUTPUT_FILE)

print("\nCorrelation Matrix:")
print(corr_matrix.round(3))

print(f"\nSaved: {OUTPUT_FILE}")