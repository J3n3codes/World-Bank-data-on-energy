from pathlib import Path
import pandas as pd

CLEAN_DATA_DIR = Path("data/clean")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/tables")

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    population = pd.read_csv(
        CLEAN_DATA_DIR / "population.csv"
    )

    gdp = pd.read_csv(
        CLEAN_DATA_DIR / "gdp_per_capita.csv"
    )

    electricity = pd.read_csv(
        CLEAN_DATA_DIR / "electricity_access.csv"
    )

    population = population.rename(
        columns={"value": "population"}
    )

    gdp = gdp.rename(
        columns={"value": "gdp_per_capita"}
    )

    electricity = electricity.rename(
        columns={"value": "electricity_access"}
    )

    population = population[
        ["country_name", "country_code", "year", "population"]
    ]

    gdp = gdp[
        ["country_name", "country_code", "year", "gdp_per_capita"]
    ]

    electricity = electricity[
        ["country_name", "country_code", "year", "electricity_access"]
    ]

    panel = population.merge(
        gdp,
        on=["country_name", "country_code", "year"],
        how="outer"
    )

    panel = panel.merge(
        electricity,
        on=["country_name", "country_code", "year"],
        how="outer"
    )

    panel = panel.sort_values(
        ["country_name", "year"]
    )

    output_file = (
        PROCESSED_DATA_DIR /
        "world_bank_panel.csv"
    )

    panel.to_csv(output_file, index=False)

    audit_report = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Countries",
            "Years",
            "Missing Country Codes",
            "Missing Population",
            "Missing GDP Per Capita",
            "Missing Electricity Access"
        ],
        "Value": [
            len(panel),
            len(panel.columns),
            panel["country_name"].nunique(),
            panel["year"].nunique(),
            panel["country_code"].isna().sum(),
            panel["population"].isna().sum(),
            panel["gdp_per_capita"].isna().sum(),
            panel["electricity_access"].isna().sum()
        ]
    })

    audit_report.to_csv(
        OUTPUT_DIR / "panel_quality_report.csv",
        index=False
    )

    print(panel.head())

    print("\nShape:")
    print(panel.shape)

    print(f"\nSaved: {output_file}")
    print("Saved: outputs/tables/panel_quality_report.csv")


if __name__ == "__main__":
    main()