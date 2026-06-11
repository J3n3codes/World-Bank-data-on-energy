from pathlib import Path
import pandas as pd

PANEL_FILE = Path("data/processed/world_bank_panel.csv")

df = pd.read_csv(PANEL_FILE)

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOUNTRIES / ENTITIES")
print(df["country_name"].nunique())

print("\nYEAR RANGE")
print(df["year"].min(), "-", df["year"].max())

print("\nMISSING VALUES")
print(df.isna().sum())

print("\nSUMMARY STATISTICS")
print(df.describe())
