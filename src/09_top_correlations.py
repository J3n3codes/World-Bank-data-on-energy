import pandas as pd
import numpy as np

corr = pd.read_csv(
    "outputs/tables/correlation_matrix.csv",
    index_col=0
)

corr_long = (
    corr.where(
        ~np.tril(
            np.ones(corr.shape)
        ).astype(bool)
    )
    .stack()
    .reset_index()
)

corr_long.columns = [
    "variable_1",
    "variable_2",
    "correlation"
]

corr_long["abs_corr"] = (
    corr_long["correlation"].abs()
)

corr_long = corr_long.sort_values(
    "abs_corr",
    ascending=False
)

corr_long.to_csv(
    "outputs/tables/top_correlations.csv",
    index=False
)

print("\nTop Correlations:\n")
print(
    corr_long.head(20).to_string(index=False)
)

print(
    "\nSaved: outputs/tables/top_correlations.csv"
)