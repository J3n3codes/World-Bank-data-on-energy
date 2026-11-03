
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Load country-level World Bank data
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/world_bank_panel.csv"
)

df = df[df["country_code"].notna()].copy()


# --------------------------------------------------
# 2. Configure output directory
# --------------------------------------------------

OUTPUT_DIR = Path("outputs/figures/bivariable")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 3. Define the seven relationships
# --------------------------------------------------

relationships = [
    {
        "x": "electricity_access",
        "y": "gdp_per_capita",
        "filename": "01_gdp_vs_electricity.png",
        "title": "GDP per Capita vs Electricity Access",
    },
    {
        "x": "electricity_access",
        "y": "life_expectancy",
        "filename": "02_electricity_vs_life_expectancy.png",
        "title": "Electricity Access vs Life Expectancy",
    },
    {
        "x": "electricity_access",
        "y": "infant_mortality",
        "filename": "03_electricity_vs_infant_mortality.png",
        "title": "Electricity Access vs Infant Mortality",
    },
    {
        "x": "drinking_water_access",
        "y": "infant_mortality",
        "filename": "04_water_vs_infant_mortality.png",
        "title": "Drinking Water Access vs Infant Mortality",
    },
    {
        "x": "drinking_water_access",
        "y": "life_expectancy",
        "filename": "05_water_vs_life_expectancy.png",
        "title": "Drinking Water Access vs Life Expectancy",
    },
    {
        "x": "gdp_per_capita",
        "y": "secondary_enrollment",
        "filename": "06_gdp_vs_secondary_enrollment.png",
        "title": "GDP per Capita vs Secondary Enrollment",
    },
    {
        "x": "internet_users",
        "y": "mobile_subscriptions",
        "filename": "07_internet_vs_mobile.png",
        "title": "Internet Users vs Mobile Subscriptions",
    },
]


# --------------------------------------------------
# 4. Define readable axis labels
# --------------------------------------------------

labels = {
    "gdp_per_capita": "GDP per capita (US$)",
    "electricity_access": "Electricity access (%)",
    "life_expectancy": "Life expectancy (years)",
    "infant_mortality": "Infant mortality rate",
    "drinking_water_access": "Drinking water access (%)",
    "secondary_enrollment": "Secondary enrollment (%)",
    "internet_users": "Internet users (%)",
    "mobile_subscriptions": "Mobile subscriptions (per 100 people)",
}


# --------------------------------------------------
# 5. Generate scatterplots
# --------------------------------------------------

results = []

for item in relationships:

    x_col = item["x"]
    y_col = item["y"]

    # Keep observations where both variables are available
    plot_data = df[[x_col, y_col]].copy()

    plot_data[x_col] = pd.to_numeric(
        plot_data[x_col], errors="coerce"
    )
    plot_data[y_col] = pd.to_numeric(
        plot_data[y_col], errors="coerce"
    )

    plot_data = plot_data.replace(
        [np.inf, -np.inf], np.nan
    ).dropna()

    x = plot_data[x_col]
    y = plot_data[y_col]

    n = len(plot_data)

    if n < 3:
        print(
            f"Skipped {item['title']}: "
            f"only {n} paired observations."
        )
        continue

    # Calculate correlations
    pearson_r = x.corr(y, method="pearson")
    spearman_r = x.corr(y, method="spearman")

    results.append({
        "variable_1": x_col,
        "variable_2": y_col,
        "pearson_r": pearson_r,
        "spearman_r": spearman_r,
        "sample_size": n,
    })

    # Create figure
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        x,
        y,
        color="#7C3AED",
        alpha=0.30,
        s=20,
        edgecolors="none",
        label="Country-year observations",
    )

    # Add linear trend line
    if x.nunique() > 1:
        slope, intercept = np.polyfit(x, y, 1)

        x_line = np.linspace(x.min(), x.max(), 200)
        y_line = slope * x_line + intercept

        ax.plot(
            x_line,
            y_line,
            color="#4C1D95",
            linewidth=2.5,
            label="Linear trend",
        )

    # Add correlation information
    annotation = (
        f"Pearson r = {pearson_r:.3f}\n"
        f"Spearman ρ = {spearman_r:.3f}\n"
        f"Paired observations (n) = {n:,}"
    )

    ax.text(
        0.03,
        0.97,
        annotation,
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=10,
        bbox={
            "boxstyle": "round,pad=0.5",
            "facecolor": "#EDE9FE",
            "edgecolor": "#A78BFA",
            "alpha": 0.90,
        },
    )

    ax.set_title(
        item["title"] + "\nCountry-level observations, 2000–2025",
        fontsize=13,
        fontweight="bold",
        color="#4C1D95",
    )

    ax.set_xlabel(labels[x_col], fontsize=11)
    ax.set_ylabel(labels[y_col], fontsize=11)

    ax.grid(
        True,
        linestyle="--",
        alpha=0.25,
    )

    ax.legend(loc="best", frameon=False)

    fig.tight_layout()

    # Save figure
    output_path = OUTPUT_DIR / item["filename"]

    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(
        f"Created: {output_path} | "
        f"Pearson r = {pearson_r:.3f} | "
        f"Spearman rho = {spearman_r:.3f} | "
        f"n = {n:,}"
    )


# --------------------------------------------------
# 6. Save correlation summary
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    "outputs/tables/selected_bivariable_relationships.csv",
    index=False,
)

print("\nScatterplot generation completed.")
print(f"Figures saved in: {OUTPUT_DIR}")
print("Correlation summary saved in outputs/tables/")


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