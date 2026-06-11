<<<<<<< HEAD

=======
from pathlib import Path
import pandas as pd

INPUT_FILE = Path(
    "data/processed/world_bank_panel.csv"
)

OUTPUT_FILE = Path(
    "data/processed/world_bank_analysis_panel.csv"
)

df = pd.read_csv(INPUT_FILE)

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

analysis_df = df[analysis_columns]

analysis_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Shape:")
print(analysis_df.shape)

print("\nMissing Values:")
print(analysis_df.isna().sum())

print(f"\nSaved: {OUTPUT_FILE}")
>>>>>>> 34780dc (Create analysis subset with core indicators)
