from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/world_bank_analysis_panel.csv")
OUTPUT_FILE = Path("outputs/tables/yearly_correlations.csv")

df = pd.read_csv(INPUT_FILE)

df = df[df["country_code"].notna()]

relationships = [
    ("electricity_access", "life_expectancy"),
    ("drinking_water_access", "life_expectancy"),
    ("internet_users", "life_expectancy"),
    ("mobile_subscriptions", "internet_users"),
    ("infant_mortality", "life_expectancy")
]

results = []

for x_var, y_var in relationships:

    temp = df[["year", x_var, y_var]].dropna()

    for year in sorted(temp["year"].unique()):

        year_df = temp[temp["year"] == year]

        corr = year_df[x_var].corr(year_df[y_var])

        results.append({
            "year": year,
            "x_variable": x_var,
            "y_variable": y_var,
            "correlation": round(corr, 3),
            "n_observations": len(year_df)
        })

results_df = pd.DataFrame(results)

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)



print("\nFirst 20 rows:\n")
print(results_df.head(20).to_string(index=False))

print(f"\nSaved: {OUTPUT_FILE}")

