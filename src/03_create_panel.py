from pathlib import Path
from functools import reduce
import pandas as pd

CLEAN_DATA_DIR = Path("data/clean")
PROCESSED_DATA_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/tables")

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_indicator_file(file_path):
    indicator_name = file_path.stem

    df = pd.read_csv(file_path)

    df = df[
        ["country_name", "country_code", "year", "value"]
    ]

    df = df.rename(
        columns={"value": indicator_name}
    )

    return df


def main():
    clean_files = sorted(CLEAN_DATA_DIR.glob("*.csv"))

    datasets = []

    for file_path in clean_files:
        df = load_indicator_file(file_path)
        datasets.append(df)
        print(f"Loaded: {file_path.name}")

    panel = reduce(
        lambda left, right: pd.merge(
            left,
            right,
            on=["country_name", "country_code", "year"],
            how="outer"
        ),
        datasets
    )

    panel = panel.sort_values(
        ["country_name", "year"]
    )

    output_file = PROCESSED_DATA_DIR / "world_bank_panel.csv"
    panel.to_csv(output_file, index=False)

    missing_report = pd.DataFrame({
        "column": panel.columns,
        "missing_count": panel.isna().sum().values,
        "missing_percent": (panel.isna().mean() * 100).round(2).values
    })

    missing_report.to_csv(
        OUTPUT_DIR / "panel_quality_report.csv",
        index=False
    )

    print("\nPanel preview:")
    print(panel.head())

    print("\nShape:")
    print(panel.shape)

    print("\nSaved:")
    print(output_file)
    print(OUTPUT_DIR / "panel_quality_report.csv")


if __name__ == "__main__":
    main()