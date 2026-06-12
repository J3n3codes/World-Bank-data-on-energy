from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path("data/processed/world_bank_analysis_panel.csv")
OUTPUT_DIR = Path("outputs/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

x_var = "electricity_access"
y_var = "life_expectancy"

df = df[
    df["country_code"].notna()
][["country_name", "year", x_var, y_var]].dropna()

years = sorted(df["year"].unique())

fig, axes = plt.subplots(
    nrows=6,
    ncols=5,
    figsize=(22, 26),
    sharex=True,
    sharey=True
)

axes = axes.flatten()

for i, year in enumerate(years):
    ax = axes[i]

    temp = df[df["year"] == year]

    ax.scatter(
        temp[x_var],
        temp[y_var],
        alpha=0.45,
        s=18
    )

    if len(temp) > 2:
        x = temp[x_var]
        y = temp[y_var]

        slope, intercept = np.polyfit(x, y, 1)
        x_line = np.linspace(x.min(), x.max(), 100)
        y_line = slope * x_line + intercept

        ax.plot(x_line, y_line)

        corr = x.corr(y)
        ax.set_title(f"{year} | r={corr:.2f}", fontsize=10)
    else:
        ax.set_title(str(year), fontsize=10)

    ax.set_xlim(0, 105)
    ax.set_ylim(35, 90)
    ax.grid(True, alpha=0.25)

for j in range(len(years), len(axes)):
    axes[j].axis("off")

fig.suptitle(
    "Life Expectancy vs Electricity Access by Year",
    fontsize=22,
    y=0.995
)

fig.supxlabel("Electricity Access (% of population)", fontsize=16)
fig.supylabel("Life Expectancy at Birth (Years)", fontsize=16)

plt.tight_layout()

png_file = OUTPUT_DIR / "life_expectancy_vs_electricity_access_yearly_grid.png"
pdf_file = OUTPUT_DIR / "life_expectancy_vs_electricity_access_yearly_grid.pdf"

plt.savefig(png_file, dpi=300, bbox_inches="tight")
plt.savefig(pdf_file, bbox_inches="tight")

print(f"Saved: {png_file}")
print(f"Saved: {pdf_file}")