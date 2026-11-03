from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path(
    "data/processed/world_bank_analysis_panel_with_regions.csv"
)

OUTPUT_DIR = Path(
    "outputs/figures/yearly_grids_by_region"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

x_var = "electricity_access"
y_var = "life_expectancy"

df = df[df["country_code"].notna()]
df = df[df["region"].notna()]

df = df[
    ["country_name", "region", "year", x_var, y_var]
].dropna()

years = sorted(df["year"].unique())

regions = [
    "East Asia & Pacific",
    "Europe & Central Asia",
    "Latin America & Caribbean",
    "Middle East, North Africa, Afghanistan & Pakistan",
    "North America",
    "South Asia",
    "Sub-Saharan Africa"
]

colors = {
    "East Asia & Pacific": "#1f77b4",
    "Europe & Central Asia": "#ff7f0e",
    "Latin America & Caribbean": "#2ca02c",
    "Middle East, North Africa, Afghanistan & Pakistan": "#d62728",
    "North America": "#9467bd",
    "South Asia": "#8c564b",
    "Sub-Saharan Africa": "#e377c2"
}

fig, axes = plt.subplots(
    nrows=13,
    ncols=2,
    figsize=(20, 60),
    sharex=True,
    sharey=True
)

axes = axes.flatten()

for i, year in enumerate(years):

    ax = axes[i]

    temp = df[df["year"] == year]

    for region in regions:

        region_df = temp[temp["region"] == region]

        ax.scatter(
            region_df[x_var],
            region_df[y_var],
            color=colors[region],
            alpha=0.65,
            s=14,
            label=region
        )

    corr = temp[x_var].corr(temp[y_var])

    ax.set_title(
        f"{year} | r={corr:.2f}",
        fontsize=13
    )

    ax.set_xlim(40, 101)
    ax.set_xticks(range(40, 102, 3))

    ax.set_ylim(25, 95)

    ax.grid(True, alpha=0.22)

for j in range(len(years), len(axes)):
    axes[j].axis("off")

handles, labels = axes[0].get_legend_handles_labels()

unique = dict(zip(labels, handles))

fig.legend(
    unique.values(),
    unique.keys(),
    loc="lower center",
    ncol=3,
    fontsize=11
)

fig.suptitle(
    "Life Expectancy vs Electricity Access by Year\nColored by World Bank Region",
    fontsize=24,
    y=0.995
)

fig.supxlabel(
    "Electricity Access (% of Population)",
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
    bottom=0.08,
    wspace=0.12,
    hspace=0.38
)

png_file = OUTPUT_DIR / (
    "life_expectancy_vs_electricity_access_region_colored.png"
)

pdf_file = OUTPUT_DIR / (
    "life_expectancy_vs_electricity_access_region_colored.pdf"
)

plt.savefig(png_file, dpi=400, bbox_inches="tight")
plt.savefig(pdf_file, bbox_inches="tight")

print(f"Saved: {png_file}")
print(f"Saved: {pdf_file}")