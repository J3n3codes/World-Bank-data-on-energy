from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = Path("data/processed/world_bank_analysis_panel.csv")
OUTPUT_DIR = Path("outputs/figures/yearly_grids")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)
df = df[df["country_code"].notna()]

PLOTS = [
    ("electricity_access", "life_expectancy"),
    ("drinking_water_access", "life_expectancy"),
    ("internet_users", "life_expectancy"),
    ("mobile_subscriptions", "internet_users"),
    ("infant_mortality", "life_expectancy"),
]


def make_yearly_grid(x_var, y_var):
    plot_df = df[["country_name", "year", x_var, y_var]].dropna()
    years = sorted(plot_df["year"].unique())

    fig, axes = plt.subplots(
        nrows=13,
        ncols=2,
        figsize=(18, 60),
        sharex=True,
        sharey=True
    )

    axes = axes.flatten()

    for i, year in enumerate(years):
        ax = axes[i]
        temp = plot_df[plot_df["year"] == year]

        ax.scatter(
            temp[x_var],
            temp[y_var],
            alpha=0.45,
            s=10
        )

        corr = temp[x_var].corr(temp[y_var])

        ax.set_title(
            f"{year} | r={corr:.2f}",
            fontsize=13
        )

        ax.grid(True, alpha=0.22)

    for j in range(len(years), len(axes)):
        axes[j].axis("off")

    fig.suptitle(
        f"{y_var.replace('_', ' ').title()} vs {x_var.replace('_', ' ').title()} by Year",
        fontsize=26,
        y=0.995
    )

    fig.supxlabel(
        x_var.replace("_", " ").title(),
        fontsize=18
    )

    fig.supylabel(
        y_var.replace("_", " ").title(),
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

    file_stub = f"{y_var}_vs_{x_var}_yearly_grid"

    png_file = OUTPUT_DIR / f"{file_stub}.png"
    pdf_file = OUTPUT_DIR / f"{file_stub}.pdf"

    plt.savefig(png_file, dpi=400, bbox_inches="tight")
    plt.savefig(pdf_file, bbox_inches="tight")
    plt.close()

    print(f"Saved: {png_file}")
    print(f"Saved: {pdf_file}")


def main():
    for x_var, y_var in PLOTS:
        make_yearly_grid(x_var, y_var)


if __name__ == "__main__":
    main()