from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path("data/processed/world_bank_analysis_panel.csv")
OUTPUT_DIR = Path("outputs/figures/yearly_grids_log")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df = df[df["country_code"].notna()]
df = df[["country_name", "year", "electricity_access", "life_expectancy"]].dropna()

df["log_electricity_gap"] = np.log(101 - df["electricity_access"])

years = sorted(df["year"].unique())

fig, axes = plt.subplots(
    nrows=13,
    ncols=2,
    figsize=(18, 60),
    sharex=True,
    sharey=True
)

axes = axes.flatten()

xmin = df["log_electricity_gap"].min()
xmax = df["log_electricity_gap"].max()

for i, year in enumerate(years):
    ax = axes[i]
    temp = df[df["year"] == year]

    x = temp["log_electricity_gap"] + np.random.normal(
        loc=0,
        scale=0.03,
        size=len(temp)
    )

    ax.scatter(
        x,
        temp["life_expectancy"],
        alpha=0.55,
        s=12
    )

    corr = temp["log_electricity_gap"].corr(temp["life_expectancy"])

    ax.set_title(
        f"{year} | r={corr:.2f}",
        fontsize=13
    )

    ax.set_xticks(np.linspace(xmin, xmax, 21))
    ax.tick_params(axis="x", labelsize=7)

    ax.grid(True, alpha=0.22)

fig.suptitle(
    "Life Expectancy vs Log Electricity Access Gap by Year",
    fontsize=26,
    y=0.995
)

fig.supxlabel(
    "log(101 - Electricity Access)",
    fontsize=18
)

fig.supylabel(
    "Life Expectancy at Birth (Years)",
    fontsize=18
)

plt.subplots_adjust(
    left=0.08,
    right=0.98,
    top=0.975,
    bottom=0.035,
    wspace=0.12,
    hspace=0.38
)

png_file = OUTPUT_DIR / "life_expectancy_vs_log_electricity_gap_yearly_grid.png"
pdf_file = OUTPUT_DIR / "life_expectancy_vs_log_electricity_gap_yearly_grid.pdf"

plt.savefig(png_file, dpi=400, bbox_inches="tight")
plt.savefig(pdf_file, bbox_inches="tight")

print(f"Saved: {png_file}")
print(f"Saved: {pdf_file}")