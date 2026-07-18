# Raw data requirements

The surviving reference workbook contains final scores rather than all six raw
component columns. To run `scripts/run_full_analysis.py`, provide a CSV with one
row per local authority and these columns:

| Column | Definition |
| --- | --- |
| `local_authority` | Local authority name |
| `online_pct` | Share of completed household returns submitted online |
| `paper_first_pct` | Share of LSOAs allocated paper-first |
| `aged_65_74_pct` | Residents aged 65 to 74 as a percentage |
| `aged_75_plus_pct` | Residents aged 75 and over as a percentage |
| `deprived_2plus_pct` | Households deprived in two or more dimensions |
| `limited_english_pct` | Residents with limited English proficiency |

The script calculates the sixth component, `underperformance`, as expected
online share minus actual online share.

Official sources documented in the report:

- ONS online-share and paper-first LSOA dataset:
  https://www.ons.gov.uk/peoplepopulationandcommunity/householdcharacteristics/homeinternetandsocialmediausage/datasets/census2021onlineshareofhouseholdresponsesbylowerlayersuperoutputareaforenglandandwales
- Nomis Census 2021 bulk data downloads:
  https://www.nomisweb.co.uk/sources/census_2021_bulk
- TS007A: age by five-year age bands
- TS011: households by deprivation dimensions
- TS029: proficiency in English

Do not commit personal, restricted or client-confidential data.

