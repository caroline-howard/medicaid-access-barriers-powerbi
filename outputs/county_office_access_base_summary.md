# County Office Access Base Summary

- Boundary/reference source: U.S. Census cartographic boundary county shapefile, cb_2025_us_county_500k
- Boundary file URL: `https://www2.census.gov/geo/tiger/GENZ2025/shp/cb_2025_us_county_500k.zip`
- Office input file: `data/processed/medicaid_offices_with_county.csv`
- County base output: `data/processed/county_office_access_base.csv`
- State base output: `data/processed/state_office_access_base.csv`
- Total counties/county equivalents: 3144
- Total offices counted: 3027
- Counties with office: 2411
- Counties without office: 733
- States/DC represented: 51
- Date/time run: 2026-06-25T14:20:09-04:00

## Top 10 States By Office Count

- TX: 248 offices
- CA: 239 offices
- GA: 157 offices
- KY: 132 offices
- MO: 125 offices
- VA: 121 offices
- MN: 109 offices
- NC: 104 offices
- IN: 102 offices
- IA: 100 offices

## Top 10 States By Share Of Counties Without An Office

- WY: 0.956522 (22 of 23 counties)
- VT: 0.928571 (13 of 14 counties)
- LA: 0.84375 (54 of 64 counties)
- AL: 0.835821 (56 of 67 counties)
- AK: 0.666667 (20 of 30 counties)
- MT: 0.660714 (37 of 56 counties)
- KS: 0.657143 (69 of 105 counties)
- MS: 0.646341 (53 of 82 counties)
- ID: 0.613636 (27 of 44 counties)
- NE: 0.602151 (56 of 93 counties)

## Notes

This table uses the same Census cartographic county boundary source as the county assignment step and includes counties with zero Medicaid offices. It covers the 50 states and D.C. only, matching the geography of the Medicaid office dataset. State-level office counts are based on assigned county geography, not the original source `state` field.
