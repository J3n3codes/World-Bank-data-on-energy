from pathlib import Path
import pandas as pd

PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/tables")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AGGREGATE_ENTITIES = [
    "North America",
    "World",
    "High income",
    "Low income",
    "Lower middle income",
    "Upper middle income",
    "Not classified",
]


def main():
    panel = pd.read_csv(PROCESSED_DATA_DIR / "world_bank_panel.csv")

    print("Panel shape:")
    print(panel.shape)

    print("\nYear range:")
    print(panel["year"].min(), "-", panel["year"].max())

    print("\nNumber of countries/entities:")
    print(panel["country_name"].nunique())

    print("\nMissing values:")
    print(panel.isna().sum())

    latest_gdp_year = panel.loc[
        panel["gdp_per_capita"].notna(),
        "year"
    ].max()

    print("\nLatest year with GDP per capita data:")
    print(latest_gdp_year)

    country_level_data = panel[
        (panel["country_code"].notna()) &
        (~panel["country_name"].isin(AGGREGATE_ENTITIES))
    ]

    data_latest = country_level_data[
        (country_level_data["year"] == latest_gdp_year) &
        (country_level_data["gdp_per_capita"].notna())
    ]

    top10_gdp = data_latest.sort_values(
        "gdp_per_capita",
        ascending=False
    ).head(10)

    bottom10_gdp = data_latest.sort_values(
        "gdp_per_capita",
        ascending=True
    ).head(10)

    top_file = OUTPUT_DIR / f"top10_gdp_per_capita_{latest_gdp_year}.csv"
    bottom_file = OUTPUT_DIR / f"bottom10_gdp_per_capita_{latest_gdp_year}.csv"

    top10_gdp.to_csv(top_file, index=False)
    bottom10_gdp.to_csv(bottom_file, index=False)

    print(f"\nTop 10 GDP per capita countries in {latest_gdp_year}:")
    print(top10_gdp[["country_name", "gdp_per_capita"]].to_string(index=False))

    print(f"\nBottom 10 GDP per capita countries in {latest_gdp_year}:")
    print(bottom10_gdp[["country_name", "gdp_per_capita"]].to_string(index=False))

    print("\nSaved:")
    print(top_file)
    print(bottom_file)


if __name__ == "__main__":
    main()