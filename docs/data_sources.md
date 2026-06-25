# Data Sources

This file documents the planned source inventory for the Medicaid Access Barriers Power BI project. Raw data files should remain unchanged in `data/raw/`; cleaning and derived outputs should be created by scripts in later milestones.

## A. Medicaid Office Locations

- Source: Shafer et al. 2024 / Harvard Dataverse
- Article: "A dataset of geocoded Medicaid office locations in the United States"
- DOI: `10.7910/DVN/AVRHMI`
- Expected file: `data/raw/medicaid_offices.xlsx`
- First cleaned analytic file: `data/processed/medicaid_offices_clean.csv`
- Purpose: Core office location dataset
- Key fields: state, address, latitude, longitude
- Expected columns: `state_fips`, `state_name`, `agency_name`, `street1`, `street2`, `city`, `state`, `zip_code`, `latitude`, `longitude`
- Limitation: Point-in-time dataset current as of late 2023; not a live office locator
- Status: Not added yet

## B. County Boundaries

- Source: U.S. Census cartographic boundary county shapefile, `cb_2025_us_county_500k`
- Purpose: Assign offices to counties and support county-level mapping
- Expected use: Spatial join using office latitude/longitude points against county polygons
- Expected output: County FIPS, county name, and county state abbreviation for each office
- Limitations: County-level geography supports broad access summaries but can hide within-county travel variation, especially in large rural counties and dense urban counties. Boundary vintages may differ from the office dataset date, and a small number of coastal or boundary-edge points may fail to match generalized cartographic polygons.
- Manual review note: One office required a documented manual county assignment because generalized county boundaries did not match the point after direct spatial join and nearest-county fallback.
- Status: Used by `scripts/03_assign_offices_to_counties.py`

## C. ACS County Indicators

- Source: American Community Survey 5-year county-level data
- Purpose: Poverty, vehicle access, broadband/internet access, language, disability, age, and other access-barrier indicators
- Note: Exact variables will be finalized in a later PR
- Status: Not added yet

## D. CMS Medicaid Enrollment

- Source: Medicaid.gov or CMS Medicaid/CHIP enrollment data
- Purpose: State-level enrollment context and office-per-enrollee indicators
- Note: County-level Medicaid enrollment may not be consistently available nationally
- Status: Not added yet

## E. Rural-Urban Classification

- Source: NCHS Urban-Rural Classification, RUCA, or USDA rural-urban data
- Purpose: Identify rural counties and compare access barriers by geography
- Status: Not added yet

## F. Optional Social Vulnerability Index

- Source: CDC/ATSDR SVI
- Purpose: Optional composite vulnerability context
- Note: Use only if it adds value and does not duplicate ACS indicators
- Status: Not added yet
