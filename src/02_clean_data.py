from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw")
CLEAN_DATA_DIR = Path("data/clean")
OUTPUT_DIR = Path("outputs/tables")

CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_dataset(file_path):
    df = pd.read_csv(file_path)

    df.columns = df.columns.str.lower().str.strip()

    df = df.sort_values(["country_name", "year"])

    clean_file_path = CLEAN_DATA_DIR / file_path.name
    df.to_csv(clean_file_path, index=False)

    audit_result = {
        "dataset": file_path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "countries": df["country_name"].nunique(),
        "missing_country_code": df["country_code"].isna().sum(),
        "missing_value": df["value"].isna().sum(),
        "percent_missing_value": round(df["value"].isna().mean() * 100, 2),
    }

    print(f"Clean copy saved: {clean_file_path}")

    return audit_result


def main():
    audit_results = []

    raw_files = list(RAW_DATA_DIR.glob("*.csv"))

    for file_path in raw_files:
        result = clean_dataset(file_path)
        audit_results.append(result)

    audit_df = pd.DataFrame(audit_results)

    audit_df.to_csv(
        OUTPUT_DIR / "data_quality_report.csv",
        index=False
    )

    cleaning_log = OUTPUT_DIR / "cleaning_log.txt"

    with open(cleaning_log, "w") as file:
        file.write("Cleaning Log\n")
        file.write("====================\n\n")
        file.write("Raw files were preserved and not modified.\n")
        file.write("Clean copies were saved in data/clean/.\n")
        file.write("Missing values were retained as pandas NaN.\n")
        file.write("No rows were deleted.\n")
        file.write("Aggregate groups were retained for now.\n")
        file.write("Rows were sorted by country_name and year.\n")

    print(f"Saved audit report: {OUTPUT_DIR / 'data_quality_report.csv'}")
    print(f"Saved cleaning log: {cleaning_log}")


if __name__ == "__main__":
    main()