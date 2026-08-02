from pathlib import Path
import requests
import pandas as pd

INPUT_FILE = Path("data/processed/world_bank_analysis_panel.csv")

OUTPUT_FILE = Path(
    "data/processed/world_bank_analysis_panel_with_regions.csv"
)

REGION_FILE = Path(
    "outputs/tables/world_bank_country_regions.csv"
)

df = pd.read_csv(INPUT_FILE)

url = "https://api.worldbank.org/v2/country?format=json&per_page=400"

response = requests.get(url, timeout=30)
response.raise_for_status()

countries = response.json()[1]

rows = []

for country in countries:
    rows.append({
        "country_code": country["id"],
        "country_name_wb": country["name"],
        "region": country["region"]["value"],
        "income_level": country["incomeLevel"]["value"]
    })

metadata = pd.DataFrame(rows)

metadata.to_csv(REGION_FILE, index=False)

merged = df.merge(
    metadata[["country_code", "region", "income_level"]],
    on="country_code",
    how="left"
)

merged.to_csv(OUTPUT_FILE, index=False)

print("\nSaved:")
print(OUTPUT_FILE)
print(REGION_FILE)

print("\nRegion counts:")
print(merged["region"].value_counts(dropna=False))