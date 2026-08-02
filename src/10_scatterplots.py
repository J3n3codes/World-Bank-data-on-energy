from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/world_bank_analysis_panel.csv"
)

OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

plots = [
    (
        "electricity_access",
        "life_expectancy"
    ),
    (
        "drinking_water_access",
        "life_expectancy"
    ),
    (
        "internet_users",
        "life_expectancy"
    )
]

for x, y in plots:

    plt.figure(figsize=(8,6))

    plt.scatter(
        df[x],
        df[y],
        alpha=0.4
    )

    plt.xlabel(x)
    plt.ylabel(y)

    plt.title(
        f"{y} vs {x}"
    )

    filename = (
        OUTPUT_DIR /
        f"{y}_vs_{x}.png"
    )

    plt.savefig(
        filename,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {filename}"
    )