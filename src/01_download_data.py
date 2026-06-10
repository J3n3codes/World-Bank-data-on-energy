"""
Download World Bank indicator data using the World Bank API.

Raw data is saved to:
data/raw/
"""

from pathlib import Path
import requests
import pandas as pd


RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

START_YEAR = 2000
END_YEAR = 2025

INDICATORS = {
    "gdp_per_capita": "NY.GDP.PCAP.CD",
    "population": "SP.POP.TOTL",
    "electricity_access": "EG.ELC.ACCS.ZS",
    "internet_users": "IT.NET.USER.ZS",
    "life_expectancy": "SP.DYN.LE00.IN",
    "renewable_energy": "EG.FEC.RNEW.ZS",
    "urban_population_percent": "SP.URB.TOTL.IN.ZS",
    "infant_mortality": "SP.DYN.IMRT.IN",
    "mobile_subscriptions": "IT.CEL.SETS.P2",
    "secondary_enrollment": "SE.SEC.ENRR",
    "smoking_male": "SH.PRV.SMOK.MA",
    "smoking_female": "SH.PRV.SMOK.FE",
    "alcohol_consumption": "SH.ALC.PCAP.LI",
    "drinking_water_access": "SH.H2O.BASW.ZS",
    "diabetes_prevalence": "SH.STA.DIAB.ZS",
}


def download_indicator(indicator_name, indicator_code):
    """
    Download one World Bank indicator for all countries.
    """

    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}"
        f"?source=2&format=json&date={START_YEAR}:{END_YEAR}&per_page=20000"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if len(data) < 2:
        raise ValueError(f"No data returned for {indicator_name}")

    records = data[1]

    rows = []

    for record in records:
        rows.append(
            {
                "country_name": record["country"]["value"],
                "country_code": record["countryiso3code"],
                "year": int(record["date"]),
                "indicator_name": indicator_name,
                "indicator_code": indicator_code,
                "value": record["value"],
            }
        )

    df = pd.DataFrame(rows)

    output_path = RAW_DATA_DIR / f"{indicator_name}.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved {indicator_name}: {output_path}")


def main():
    for indicator_name, indicator_code in INDICATORS.items():
        download_indicator(indicator_name, indicator_code)


if __name__ == "__main__":
    main()
