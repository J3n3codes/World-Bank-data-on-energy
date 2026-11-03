
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ==========================================================
# 1. FILE PATHS
# ==========================================================

INPUT_FILE = Path(
    "outputs/tables/panel_inference/pooled_panel_inference.csv"
)

OUTPUT_DIR = Path("outputs/figures/panel_inference")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 2. VISUAL DESIGN
# ==========================================================

NAVY = "#17243A"
BLUE = "#3977A8"
CORAL = "#D97757"
GREY = "#64748B"
LIGHT_GREY = "#E8EDF2"
BACKGROUND = "#FFFFFF"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 9,
    "figure.facecolor": BACKGROUND,
    "axes.facecolor": BACKGROUND,
    "savefig.facecolor": BACKGROUND,
    "axes.edgecolor": LIGHT_GREY,
    "axes.labelcolor": NAVY,
    "xtick.color": GREY,
    "ytick.color": NAVY,
})


# ==========================================================
# 3. LOAD AND VALIDATE RESULTS
# ==========================================================

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "relationship",
    "x_variable",
    "y_variable",
    "model",
    "coefficient",
    "confidence_interval_lower",
    "confidence_interval_upper",
    "observations",
    "countries",
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

if df.empty:
    raise ValueError("The regression results file is empty.")

numeric_columns = [
    "coefficient",
    "confidence_interval_lower",
    "confidence_interval_upper",
    "observations",
    "countries",
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if df[numeric_columns].isna().any().any():
    raise ValueError("Missing or invalid numerical regression results.")

pooled_name = "Pooled OLS - Country Clustered SE"
fixed_name = "Country + Year Fixed Effects"

expected_models = {pooled_name, fixed_name}

if set(df["model"].unique()) != expected_models:
    raise ValueError("Unexpected model names in the results file.")

relationships = df["relationship"].drop_duplicates().tolist()

if len(relationships) != 7:
    raise ValueError(
        f"Expected 7 relationships, found {len(relationships)}."
    )

for relationship in relationships:
    subset = df[df["relationship"] == relationship]

    if set(subset["model"]) != expected_models:
        raise ValueError(
            f"Incomplete model results for: {relationship}"
        )

print("Regression results loaded successfully.")
print("Relationships:", len(relationships))


# ==========================================================
# 4. DISPLAY LABELS
# ==========================================================

variable_labels = {
    "electricity_access": "Electricity access (%)",
    "gdp_per_capita": "Log GDP per capita",
    "life_expectancy": "Life expectancy (years)",
    "infant_mortality": "Infant mortality",
    "drinking_water_access": "Drinking water access (%)",
    "secondary_enrollment": "Secondary enrollment",
    "internet_users": "Internet users (%)",
    "mobile_subscriptions": "Mobile subscriptions",
}


def get_relationship_title(row):
    x = variable_labels.get(row["x_variable"], row["x_variable"])
    y = variable_labels.get(row["y_variable"], row["y_variable"])

    return f"{x}  →  {y}"


# ==========================================================
# 5. CREATE THE COEFFICIENT PLOT
# ==========================================================

fig, axes = plt.subplots(
    nrows=4,
    ncols=2,
    figsize=(15, 17),
    constrained_layout=False
)

axes = axes.flatten()

model_styles = {
    pooled_name: {
        "color": BLUE,
        "label": "Pooled OLS",
        "position": 1,
    },
    fixed_name: {
        "color": CORAL,
        "label": "Country + year fixed effects",
        "position": 0,
    },
}


for i, relationship in enumerate(relationships):

    ax = axes[i]

    subset = df[df["relationship"] == relationship].copy()

    first_row = subset.iloc[0]
    title = get_relationship_title(first_row)

    # Use the same sample size and country count for both
    # specifications within each relationship.
    n = int(first_row["observations"])
    countries = int(first_row["countries"])

    # Draw a zero-reference line.
    ax.axvline(
        0,
        color=GREY,
        linewidth=1.1,
        linestyle="--",
        alpha=0.8,
        zorder=1,
    )

    # Draw both model estimates and confidence intervals.
    for model_name, style in model_styles.items():

        row = subset[subset["model"] == model_name].iloc[0]

        estimate = row["coefficient"]
        lower = row["confidence_interval_lower"]
        upper = row["confidence_interval_upper"]

        xerr = np.array([
            [estimate - lower],
            [upper - estimate],
        ])

        ax.errorbar(
            estimate,
            style["position"],
            xerr=xerr,
            fmt="o",
            color=style["color"],
            ecolor=style["color"],
            markersize=8,
            markeredgecolor="white",
            markeredgewidth=1.2,
            elinewidth=2.2,
            capsize=4,
            capthick=1.5,
            zorder=3,
        )

    # Panel heading.
    ax.set_title(
        title,
        loc="left",
        color=NAVY,
        pad=12,
    )

    
# Model specification labels.
ax.set_yticks([0, 1])
ax.set_yticklabels([
    r"$M_2$",
    r"$M_1$",
])

# Individual coefficient axis label.
ax.set_xlabel(
    r"Regression coefficient ($\beta$)",
    fontsize=9
)

ax.set_ylim(-0.6, 1.6)

# Independent scale for each relationship.
all_values = subset[
    [
        "confidence_interval_lower",
        "confidence_interval_upper",
    ]
    ].to_numpy().flatten()

xmin = min(all_values.min(), 0)
xmax = max(all_values.max(), 0)

span = xmax - xmin

if span == 0:
    span = max(abs(xmax), 1)

    padding = span * 0.16

    ax.set_xlim(
        xmin - padding,
        xmax + padding
    )

# Subtle horizontal gridlines.
ax.grid(
    axis="x",
    color=LIGHT_GREY,
    linewidth=0.8,
    zorder=0,
    )

ax.set_axisbelow(True)

# Clean panel borders.
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

ax.spines["bottom"].set_color(LIGHT_GREY)

ax.tick_params(
    axis="y",
    length=0,
    pad=8,
    )

ax.tick_params(
    axis="x",
    length=3,
    color=GREY,
    )

    # Sample information.
ax.text(
    0.99,
    0.04,
    f"N = {n:,}  |  Countries = {countries}",
    transform=ax.transAxes,
    ha="right",
    va="bottom",
    fontsize=8,
    color=GREY,
    )


# Remove the unused eighth panel.
axes[-1].axis("off")


# ==========================================================
# 6. FIGURE TITLE AND LEGEND
# ==========================================================

fig.suptitle(
    "GLOBAL DEVELOPMENT INDICATORS",
    x=0.075,
    y=0.975,
    ha="left",
    fontsize=20,
    fontweight="bold",
    color=NAVY,
)

fig.text(
    0.075,
    0.950,
    "Pooled associations versus country and year fixed-effects estimates",
    ha="left",
    fontsize=11,
    color=GREY,
)

fig.text(
    0.075,
    0.928,
    "Country-level panel data | 2000–2025 data coverage",
    ha="left",
    fontsize=9,
    color=GREY,
)

# Legend.
from matplotlib.lines import Line2D

legend_handles = [
    Line2D(
        [0], [0],
        marker="o",
        color=BLUE,
        markerfacecolor=BLUE,
        markersize=8,
        linewidth=2,
        label=r"$M_1$ — Pooled OLS (country-clustered SE)",
    ),
    Line2D(
        [0], [0],
        marker="o",
        color=CORAL,
        markerfacecolor=CORAL,
        markersize=8,
        linewidth=2,
        label=r"$M_2$ — Country + Year Fixed Effects",
    ),
]

fig.legend(
    handles=legend_handles,
    loc="upper right",
    bbox_to_anchor=(0.925, 0.963),
    frameon=False,
    fontsize=9,
)


# ==========================================================
# 7. METHODOLOGICAL FOOTNOTE
# ==========================================================

footnote = (
    "Points represent regression coefficients; horizontal lines represent "
    "95% confidence intervals.\n"
    "Standard errors are clustered by country. GDP per capita is "
    "log-transformed wherever used.\n"
    "Each panel has its own horizontal scale. Estimates are observational "
    "associations, not causal effects."
)

fig.text(
    0.075,
    0.025,
    footnote,
    ha="left",
    va="bottom",
    fontsize=8,
    color=GREY,
    linespacing=1.6,
)

# Layout.
# Shared axis labels.
fig.supxlabel(
    "Regression coefficient (β)",
    fontsize=12,
    fontweight="bold",
    color=NAVY,
    y=0.065,
)

fig.supylabel(
    "Model specification",
    fontsize=12,
    fontweight="bold",
    color=NAVY,
    x=0.025,
)

# Layout.
plt.subplots_adjust(
    left=0.19,
    right=0.94,
    top=0.89,
    bottom=0.14,
    hspace=0.65,
    wspace=0.35,
)



# ==========================================================
# 8. EXPORT HIGH-QUALITY OUTPUTS
# ==========================================================

png_file = (
    OUTPUT_DIR / "panel_inference_coefficient_plot.png"
)

pdf_file = (
    OUTPUT_DIR / "panel_inference_coefficient_plot.pdf"
)

fig.savefig(
    png_file,
    dpi=400,
    bbox_inches="tight",
)

fig.savefig(
    pdf_file,
    bbox_inches="tight",
)

plt.close(fig)


# ==========================================================
# 9. COMPLETION
# ==========================================================

print("\n" + "=" * 65)
print("PANEL INFERENCE VISUALIZATION COMPLETE")
print("=" * 65)

print("PNG:", png_file)
print("PDF:", pdf_file)
