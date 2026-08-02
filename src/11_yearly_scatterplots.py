from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/world_bank_analysis_panel.csv"
)

output_dir = Path(
    "outputs/figures/yearly_scatterplots"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

for year in sorted(df["year"].unique()):

    temp = df[
        df["year"] == year
    ]

    plt.figure(figsize=(8,6))

    plt.scatter(
        temp["electricity_access"],
        temp["life_expectancy"],
        alpha=0.6
    )

    plt.xlabel(
        "Electricity Access (%)"
    )

    plt.ylabel(
        "Life Expectancy (Years)"
    )

    plt.title(
        f"Life Expectancy vs Electricity Access ({year})"
    )

    plt.savefig(
        output_dir /
        f"life_expectancy_vs_electricity_access_{year}.png",
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved {year}"
    )

print("\nDone.")