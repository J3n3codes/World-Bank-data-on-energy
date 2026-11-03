
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


# --------------------------------------------------
# 1. File paths and configuration
# --------------------------------------------------

INPUT_FILE = Path("data/processed/world_bank_panel.csv")

OUTPUT_DIR = Path("outputs/tables/panel_inference")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CONFIDENCE_LEVEL = 0.95


# --------------------------------------------------
# 2. Load country-level observations
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df = df[df["country_code"].notna()].copy()

df["year"] = pd.to_numeric(df["year"], errors="coerce")

# Convert infinite values to missing values
df = df.replace([np.inf, -np.inf], np.nan)

print("=" * 70)
print("POOLED PANEL INFERENCE")
print("=" * 70)

print("Country-level observations:", len(df))
print("Unique countries:", df["country_code"].nunique())
print("Year range:", df["year"].min(), "-", df["year"].max())


# --------------------------------------------------
# 3. Define relationships
# --------------------------------------------------

relationships = [
    ("electricity_access", "gdp_per_capita"),
    ("electricity_access", "life_expectancy"),
    ("electricity_access", "infant_mortality"),
    ("drinking_water_access", "infant_mortality"),
    ("drinking_water_access", "life_expectancy"),
    ("gdp_per_capita", "secondary_enrollment"),
    ("internet_users", "mobile_subscriptions"),
]


# --------------------------------------------------
# 4. Prepare variables
# --------------------------------------------------

# Use log GDP per capita because GDP is highly skewed.
df["log_gdp_per_capita"] = np.log(
    df["gdp_per_capita"].where(df["gdp_per_capita"] > 0)
)

# Store model results
results = []


# --------------------------------------------------
# 5. Fit both regression specifications
# --------------------------------------------------

for x_var, y_var in relationships:

    # Transform GDP per capita wherever it appears
    if x_var == "gdp_per_capita":
        model_x = "log_gdp_per_capita"
    else:
        model_x = x_var

    if y_var == "gdp_per_capita":
        model_y = "log_gdp_per_capita"
    else:
        model_y = y_var

    required = [
        "country_code",
        "year",
        model_x,
        model_y
    ]

    temp = df[required].dropna().copy()

    n = len(temp)
    countries = temp["country_code"].nunique()

    print("\n" + "-" * 70)
    print(f"{x_var} vs {y_var}")
    print("Observations:", n)
    print("Countries:", countries)

    if n < 30 or countries < 10:
        print("Insufficient observations or clusters. Skipping.")
        continue

    formula = f"{model_y} ~ {model_x}"

    # ----------------------------------------------
    # Model 1: Pooled OLS, country-clustered SE
    # ----------------------------------------------

    pooled = smf.ols(
        formula=formula,
        data=temp
    ).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": temp["country_code"],
            "use_correction": True
        },
        use_t=True
    )

    # ----------------------------------------------
    # Model 2: Country and year fixed effects
    # ----------------------------------------------

    fixed_effects = smf.ols(
        formula=(
            f"{model_y} ~ {model_x} "
            "+ C(country_code) + C(year)"
        ),
        data=temp
    ).fit(
        cov_type="cluster",
        cov_kwds={
            "groups": temp["country_code"],
            "use_correction": True,
            "df_correction": True
        },
        use_t=True
    )

    # ----------------------------------------------
    # Extract results
    # ----------------------------------------------

    for model_name, model in [
        ("Pooled OLS - Country Clustered SE", pooled),
        ("Country + Year Fixed Effects", fixed_effects)
    ]:

        coefficient = model.params[model_x]
        standard_error = model.bse[model_x]
        p_value = model.pvalues[model_x]

        confidence_interval = model.conf_int(
            alpha=1 - CONFIDENCE_LEVEL
        ).loc[model_x]

        results.append({
            "relationship": f"{x_var} vs {y_var}",
            "x_variable": x_var,
            "y_variable": y_var,
            "model": model_name,
            "coefficient": coefficient,
            "clustered_standard_error": standard_error,
            "confidence_interval_lower": confidence_interval.iloc[0],
            "confidence_interval_upper": confidence_interval.iloc[1],
            "p_value": p_value,
            "observations": int(model.nobs),
            "countries": countries,
            "r_squared": model.rsquared
        })

        print(f"\n{model_name}")
        print("Coefficient:", round(coefficient, 5))
        print("Clustered SE:", round(standard_error, 5))
        print(
            "95% CI:",
            (
                round(confidence_interval.iloc[0], 5),
                round(confidence_interval.iloc[1], 5)
            )
        )
        print("P-value:", round(p_value, 6))


# --------------------------------------------------
# 6. Save results
# --------------------------------------------------

results_df = pd.DataFrame(results)

output_file = OUTPUT_DIR / "pooled_panel_inference.csv"

results_df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 70)
print("PANEL INFERENCE COMPLETE")
print("=" * 70)

print("\nResults:")
print(results_df.to_string(index=False))

print("\nSaved:", output_file)
