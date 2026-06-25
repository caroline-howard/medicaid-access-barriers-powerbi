# Data Sources

This file documents the planned source inventory for the Postpartum Medicaid Access Barriers Power BI project. Raw data files should remain unchanged in `data/raw/`; cleaning and derived outputs should be created by scripts in later milestones.

## A. Medicaid Office Locations

- Source: Shafer et al. 2024 / Harvard Dataverse
- Article: "A dataset of geocoded Medicaid office locations in the United States"
- DOI: `10.7910/DVN/AVRHMI`
- Expected file: `data/raw/medicaid_offices.xlsx`
- First cleaned analytic file: `data/processed/medicaid_offices_clean.csv`
- Purpose: Core office location dataset used to identify counties where postpartum Medicaid populations may have limited in-person administrative support availability.
- Key fields: state, address, latitude, longitude
- Expected columns: `state_fips`, `state_name`, `agency_name`, `street1`, `street2`, `city`, `state`, `zip_code`, `latitude`, `longitude`
- Limitation: Point-in-time dataset current as of late 2023; not a live office locator
- Status: Not added yet

## B. County Boundaries

- Source: U.S. Census cartographic boundary county shapefile, `cb_2025_us_county_500k`
- Purpose: Assign offices to counties and support county-level mapping of postpartum Medicaid administrative access context.
- Expected use: Spatial join using office latitude/longitude points against county polygons
- Expected output: County FIPS, county name, and county state abbreviation for each office; complete county office access base table with zero-office counties included
- Limitations: County-level geography supports broad access summaries but can hide within-county travel variation, especially in large rural counties and dense urban counties. Boundary vintages may differ from the office dataset date, and a small number of coastal or boundary-edge points may fail to match generalized cartographic polygons.
- Manual review note: One office required a documented manual county assignment because generalized county boundaries did not match the point after direct spatial join and nearest-county fallback.
- Status: Used by `scripts/03_assign_offices_to_counties.py` and `scripts/04_build_county_office_access_base.py`

## C. ACS County Indicators

- Source: American Community Survey 5-year county-level data through the Census API; `scripts/05_add_acs_access_indicators.py` discovers the most recent available ACS 5-year vintage at run time.
- Purpose: Add county-level poverty, no-vehicle household, internet subscription, limited-English, older adult, disability, and race/ethnicity context indicators to the county office access base table for postpartum access-barrier screening.
- Indicators added: total population, poverty count/rate, no-vehicle households/rate, households without internet subscription/rate, limited-English-speaking households/rate, population age 65+/rate, disability count/rate, and race/ethnicity context rates.
- Future update note: Add female population ages 15-44 or another reproductive-age population measure to provide postpartum-relevant population context.
- Limitation: ACS estimates are survey-based and county-level indicators may hide substantial within-county variation.
- Status: Added by `scripts/05_add_acs_access_indicators.py`

## D. CMS Medicaid Enrollment

- Source: Medicaid.gov or CMS Medicaid/CHIP enrollment data
- Purpose: State-level Medicaid enrollment context for interpreting the broader program environment.
- Note: State-level Medicaid enrollment may provide context but does not directly identify postpartum Medicaid enrollees. County-level Medicaid enrollment may not be consistently available nationally.
- Status: Not added yet

## E. Rural-Urban Classification

- Source: NCHS Urban-Rural Classification, RUCA, or USDA rural-urban data
- Purpose: Compare postpartum Medicaid administrative access patterns by urban-rural county type, including metro/nonmetro differences.
- Status: Not added yet

## F. Optional Social Vulnerability Index

- Source: CDC/ATSDR SVI
- Purpose: Optional composite vulnerability context
- Note: Use only if it adds value and does not duplicate ACS indicators
- Status: Not added yet

## G. Hospital-Based Obstetric Care Status

- Source: University of Minnesota Rural Health Research Center / Rural Maternal Health Data Support and Analysis Program
- Dataset: 2010-2024 County-Level Hospital-Based Obstetric Care Status
- Source page: `https://rhrc.umn.edu/publication/2010-2024-county-level-hospital-based-obstetric-care-status/`
- Source file: `https://rhrc.umn.edu/wp-content/uploads/2026/05/county_OBstat_2010_2024.xlsx`
- Purpose: Identify whether counties have hospital-based obstetric care available.
- Use in project: Postpartum-specific clinical access context and potential index component.
- Limitation: This identifies hospital-based obstetric care status, not all prenatal care, postpartum care, outpatient OB/GYN access, birth centers, doulas, midwives, community health centers, or Medicaid enrollment support.
- Status: Added by `scripts/07_add_obstetric_care_status.py`
