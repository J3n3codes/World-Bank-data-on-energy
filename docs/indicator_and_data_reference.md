
# Data Dictionary

## Project

**Analysis of Global Electricity Access and Economic Development Trends Using World Bank Data (2000–2025)**

This project uses 15 indicators retrieved from the World Bank API. The indicators cover economic development, electricity and digital access, health, education, demographics, and environmental conditions.

The primary research focus is the relationship between GDP per capita and access to electricity. The remaining indicators support exploratory descriptive and bivariate analyses.

## Indicator Reference

| Project variable | World Bank indicator code | Description | Unit / measurement |
|---|---|---|---|
| `gdp_per_capita` | `NY.GDP.PCAP.CD` | GDP per capita | Current US dollars |
| `population` | `SP.POP.TOTL` | Total population | Number of people |
| `electricity_access` | `EG.ELC.ACCS.ZS` | Access to electricity | Percentage of population |
| `internet_users` | `IT.NET.USER.ZS` | Individuals using the Internet | Percentage of population |
| `life_expectancy` | `SP.DYN.LE00.IN` | Life expectancy at birth | Years |
| `renewable_energy` | `EG.FEC.RNEW.ZS` | Renewable energy consumption | Percentage of total final energy consumption |
| `urban_population_percent` | `SP.URB.TOTL.IN.ZS` | Urban population | Percentage of total population |
| `infant_mortality` | `SP.DYN.IMRT.IN` | Infant mortality rate | Deaths per 1,000 live births |
| `mobile_subscriptions` | `IT.CEL.SETS.P2` | Mobile cellular subscriptions | Subscriptions per 100 people |
| `secondary_enrollment` | `SE.SEC.ENRR` | School enrollment, secondary | Gross enrollment ratio (%) |
| `smoking_male` | `SH.PRV.SMOK.MA` | Prevalence of tobacco use, males | Percentage of male adults |
| `smoking_female` | `SH.PRV.SMOK.FE` | Prevalence of tobacco use, females | Percentage of female adults |
| `alcohol_consumption` | `SH.ALC.PCAP.LI` | Total alcohol consumption per capita | Litres of pure alcohol per adult (15+) |
| `drinking_water_access` | `SH.H2O.BASW.ZS` | Access to at least basic drinking water services | Percentage of population |
| `diabetes_prevalence` | `SH.STA.DIAB.ZS` | Prevalence of diabetes | Percentage of adults |

## Dataset Structure

The project covers the years 2000–2025.

The full processed panel contains:

- 6,916 country/entity-year observations
- 18 columns, including identifiers and 15 indicators
- 266 entity names
- 261 unique non-null country codes
- 130 aggregate observations without country codes

The analysis subset contains 13 columns: three identifiers and ten selected indicators.

## Identifiers

| Variable | Description |
|---|---|
| `country_name` | Country or aggregate entity name |
| `country_code` | World Bank country/entity ISO3 code; missing for aggregate entities |
| `year` | Observation year |

## Missing Data and Coverage

Indicator availability varies across countries and years. Missing values are retained as `NaN`; observations are not removed from the full panel simply because one or more indicators are unavailable.

Coverage is particularly limited for diabetes prevalence and the male and female smoking indicators. Electricity access observations extend through 2023 in the retrieved dataset, while GDP per capita extends through 2024. Availability should therefore be assessed separately for each analysis.

Analytical datasets use pairwise complete observations where appropriate. Consequently, sample sizes differ between indicator relationships.

## Analytical Considerations

- GDP per capita is measured in current US dollars and is not adjusted for inflation or purchasing-power differences.
- Mobile subscriptions per 100 people and gross secondary enrollment ratios can exceed 100.
- Country-year observations are repeated measurements of countries over time.
- Pooled analyses should account for within-country dependence where inferential statistics are used.
- Correlations and regression associations do not, by themselves, establish causation.
- Aggregate entities are retained in the source and full panel but excluded from country-level analyses.

## Data Source

World Bank, World Development Indicators (WDI).

API endpoint pattern:

`https://api.worldbank.org/v2/country/all/indicator/{indicator_code}`

The project retrieves observations for 2000–2025 using the indicator codes listed above.
