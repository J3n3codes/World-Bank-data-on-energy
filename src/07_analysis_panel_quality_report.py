from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/world_bank_analysis_panel.csv")
OUTPUT_FILE = Path("outputs/tables/analysis_panel_quality_report.csv")

df = pd.read_csv(INPUT_FILE)

report = pd.DataFrame({
    "column": df.columns,
    "missing_count": df.isna().sum().values,
    "missing_percent": (df.isna().mean() * 100).round(2).values,
    "non_missing_count": df.notna().sum().values,
    "dtype": df.dtypes.astype(str).values
})

report.to_csv(OUTPUT_FILE, index=False)

print("Analysis Panel Shape:")
print(df.shape)

print("\nAnalysis Panel Quality Report:")
print(report.to_string(index=False))

print(f"\nSaved: {OUTPUT_FILE}")