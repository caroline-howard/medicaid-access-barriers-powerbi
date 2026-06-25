# County Assignment Summary

- Input file: `data/processed/medicaid_offices_clean.csv`
- Office-level output: `data/processed/medicaid_offices_with_county.csv`
- County count output: `data/processed/county_office_counts.csv`
- State summary output: `data/processed/state_office_summary.csv`
- Manual assignment crosswalk: `data/manual/manual_county_assignments.csv`
- Boundary source used: U.S. Census cartographic boundary county shapefile, cb_2025_us_county_500k
- Boundary file URL: `https://www2.census.gov/geo/tiger/GENZ2025/shp/cb_2025_us_county_500k.zip`
- Offices read: 3027
- Offices matched by direct spatial join: 3025
- Offices matched by nearest-county fallback: 1
- Offices matched by manual review crosswalk: 1
- Offices unmatched: 0
- Fallback distance threshold: 5.0 miles (8.05 km)
- Counties with at least one office: 2411
- States/DC represented: 51
- Date/time run: 2026-06-25T13:58:31-04:00

## Top 10 States By Office Count

- TX: 248
- CA: 239
- GA: 157
- KY: 132
- MO: 125
- VA: 121
- MN: 109
- NC: 104
- IN: 102
- IA: 100

## Unmatched Offices

No unmatched offices were found; `outputs/offices_without_county_match.csv` contains headers only.

## Manual Review Crosswalk

Manual county assignments are applied only after direct spatial join and nearest-county fallback fail. The crosswalk is limited to reviewed records in `data/manual/manual_county_assignments.csv` and uses `county_match_method = manual_review_crosswalk`.

## Limitations

County assignment first uses office latitude/longitude points and Census 2025 cartographic county boundaries for a direct point-in-polygon spatial join. For offices that do not fall inside a generalized county polygon, the script applies a conservative nearest-county fallback using the same boundary file only when the nearest county boundary is within 5.0 miles. Reviewed manual assignments are applied after those automated steps only. This is appropriate for county-level summaries but does not measure travel distance, within-county access variation, or whether an office serves residents across county or state lines. Boundary vintages may differ from the late-2023 office dataset. Any offices still unmatched after fallback and manual review are exported for review instead of being forced into a county.
