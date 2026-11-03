
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Border, Side, Alignment
)
from openpyxl.utils import get_column_letter


# 1. Paths and input data

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data/processed/world_bank_panel.csv"

TABLE_DIR = ROOT / "outputs/tables"
FIGURE_DIR = ROOT / "outputs/figures/univariable"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)


# 2. Define the 15 indicators

indicators = [
    "gdp_per_capita",
    "population",
    "electricity_access",
    "internet_users",
    "life_expectancy",
    "renewable_energy",
    "urban_population_percent",
    "infant_mortality",
    "mobile_subscriptions",
    "secondary_enrollment",
    "smoking_male",
    "smoking_female",
    "alcohol_consumption",
    "drinking_water_access",
    "diabetes_prevalence"
]


# 3. Separate countries and aggregate entities

country_data = df[df["country_code"].notna()].copy()
aggregate_data = df[df["country_code"].isna()].copy()

groups = {
    "country_level": country_data,
    "aggregate_entities": aggregate_data
}

print("=" * 65)
print("UNIVARIABLE ANALYSIS")
print("=" * 65)

print("Full dataset rows:", len(df))
print("Country-level rows:", len(country_data))
print("Aggregate rows:", len(aggregate_data))


# 4. Descriptive statistics

summary_rows = []

for group_name, group_data in groups.items():

    for indicator in indicators:

        values = group_data[indicator].dropna()

        row = {
            "group": group_name,
            "indicator": indicator,
            "total_rows": len(group_data),
            "valid_observations": values.count(),
            "missing_observations": group_data[indicator].isna().sum(),
            "missing_percentage": group_data[indicator].isna().mean() * 100,
            "mean": values.mean(),
            "standard_deviation": values.std(),
            "median": values.median(),
            "q1": values.quantile(0.25),
            "q3": values.quantile(0.75),
            "iqr": values.quantile(0.75) - values.quantile(0.25),
            "minimum": values.min(),
            "maximum": values.max(),
            "skewness": values.skew()
        }

        summary_rows.append(row)


summary = pd.DataFrame(summary_rows)

summary_file = TABLE_DIR / "univariable_descriptive_statistics.csv"
summary.to_csv(summary_file, index=False)


# 5. Missingness report

missingness = pd.DataFrame({
    "indicator": indicators,
    "total_observations": len(df),
    "valid_observations": [
        df[col].notna().sum() for col in indicators
    ],
    "missing_observations": [
        df[col].isna().sum() for col in indicators
    ],
    "missing_percentage": [
        df[col].isna().mean() * 100 for col in indicators
    ]
})

missingness_file = TABLE_DIR / "univariable_missingness.csv"
missingness.to_csv(missingness_file, index=False)


# 6. Frequency distributions

frequency_rows = []

for group_name, group_data in groups.items():

    for indicator in indicators:

        values = group_data[indicator].dropna()

        if values.empty:
            continue

        # Use up to 10 equal-width intervals.
        # Constant-valued indicators are handled separately.
        if values.nunique() == 1:
            frequency_rows.append({
                "group": group_name,
                "indicator": indicator,
                "interval": f"{values.iloc[0]} (constant)",
                "frequency": len(values),
                "percentage": 100.0
            })
            continue

        categories = pd.cut(
            values,
            bins=10,
            include_lowest=True,
            duplicates="drop"
        )

        counts = categories.value_counts(sort=False)

        for interval, count in counts.items():

            frequency_rows.append({
                "group": group_name,
                "indicator": indicator,
                "interval": str(interval),
                "frequency": int(count),
                "percentage": count / len(values) * 100
            })


frequency = pd.DataFrame(frequency_rows)

frequency_file = TABLE_DIR / "univariable_frequency_distributions.csv"
frequency.to_csv(frequency_file, index=False)


# 7. Create a formatted Excel workbook

excel_file = TABLE_DIR / "univariable_analysis_tables.xlsx"

with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:

    summary.to_excel(
        writer,
        sheet_name="Descriptive Statistics",
        index=False
    )

    missingness.to_excel(
        writer,
        sheet_name="Missingness",
        index=False
    )

    frequency.to_excel(
        writer,
        sheet_name="Frequency Distributions",
        index=False
    )

    workbook = writer.book

    dark_grey = "404040"
    medium_grey = "D9D9D9"
    light_grey = "F2F2F2"
    white = "FFFFFF"
    black = "000000"
    border_grey = "BFBFBF"

    thin_border = Border(
        bottom=Side(style="thin", color=border_grey)
    )

    for worksheet in workbook.worksheets:

        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        # Header styling
        for cell in worksheet[1]:
            cell.fill = PatternFill(
                "solid", fgColor=dark_grey
            )
            cell.font = Font(
                name="Arial",
                bold=True,
                color=white,
                size=10
            )
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )
            cell.border = thin_border

        worksheet.row_dimensions[1].height = 32

        # Body styling
        for row_index, row in enumerate(
            worksheet.iter_rows(min_row=2), start=2
        ):

            fill_color = (
                light_grey if row_index % 2 == 0
                else white
            )

            for cell in row:
                cell.fill = PatternFill(
                    "solid", fgColor=fill_color
                )
                cell.font = Font(
                    name="Arial",
                    color=black,
                    size=10
                )
                cell.border = thin_border
                cell.alignment = Alignment(
                    vertical="center"
                )

                if isinstance(cell.value, float):
                    cell.number_format = "#,##0.000"

        # Adjust column widths
        for column_cells in worksheet.columns:

            column_letter = get_column_letter(
                column_cells[0].column
            )

            max_length = max(
                len(str(cell.value or ""))
                for cell in column_cells
            )

            worksheet.column_dimensions[
                column_letter
            ].width = min(max(max_length + 3, 14), 32)


# 8. Country-level distribution histograms

for indicator in indicators:

    values = country_data[indicator].dropna()

    if len(values) == 0:
        continue

    plt.figure(figsize=(9, 5))

    plt.hist(
        values,
        bins=30,
        edgecolor="black",
        alpha=0.75,
        color="grey"
    )

    plt.title(
        f"Distribution of {indicator}\n"
        f"Country-level observations, n={len(values)}"
    )

    plt.xlabel(indicator)
    plt.ylabel("Frequency")

    plt.grid(axis="y", alpha=0.2)
    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / f"{indicator}_histogram.png",
        dpi=300
    )

    plt.close()


# 9. Print results

print("\nCOUNTRY-LEVEL DESCRIPTIVE STATISTICS")
print("=" * 65)

country_summary = summary[
    summary["group"] == "country_level"
]

print(
    country_summary[
        [
            "indicator",
            "valid_observations",
            "mean",
            "standard_deviation",
            "median",
            "q1",
            "q3",
            "minimum",
            "maximum",
            "skewness"
        ]
    ].round(3).to_string(index=False)
)

print("\nMISSINGNESS")
print("=" * 65)
print(missingness.round(2).to_string(index=False))

print("\nANALYSIS COMPLETE")
print("=" * 65)

print("Generated files:")
print(summary_file)
print(missingness_file)
print(frequency_file)
print(excel_file)
print(FIGURE_DIR)
