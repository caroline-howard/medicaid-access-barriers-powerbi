# Data Sources

This file documents the source inventory for the Postpartum Medicaid Access Barriers Power BI project. Raw data files should remain unchanged in `data/raw/`; cleaning and derived outputs are created by scripts.

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
- Status: Added; cleaned by `scripts/02_clean_medicaid_offices.py` and assigned to counties by `scripts/03_assign_offices_to_counties.py`

## B. County Boundaries

- Source: U.S. Census cartographic boundary county shapefile, `cb_2025_us_county_500k`
- Purpose: Assign offices to counties and support county-level mapping of postpartum Medicaid administrative access context.
- Expected use: Spatial join using office latitude/longitude points against county polygons
- Expected output: County FIPS, county name, and county state abbreviation for each office; complete county office access base table with zero-office counties included
- Limitations: County-level geography supports broad access summaries but can hide within-county travel variation, especially in large rural counties and dense urban counties. Boundary vintages may differ from the office dataset date, and a small number of coastal or boundary-edge points may fail to match generalized cartographic polygons.
- Manual review note: One office required a documented manual county assignment because generalized county boundaries did not match the point after direct spatial join and nearest-county fallback.
- Status: Used by `scripts/03_assign_offices_to_counties.py` and `scripts/04_build_county_office_access_base.py`

## C. ACS County Indicators

- Source: American Community Survey 2024 5-year county-level data through the Census API.
- Purpose: Add county-level poverty, no-vehicle household, internet subscription, limited-English, disability, female population ages 15-44, and race/ethnicity context indicators to the county office access base table for postpartum access-barrier screening.
- Indicators added: total population, poverty count/rate, no-vehicle households/rate, households without internet subscription/rate, limited-English-speaking households/rate, disability count/rate, female population ages 15-44 count/rate, and race/ethnicity context rates.
- Postpartum context note: Female population ages 15-44 is included as a postpartum-relevant reproductive-age population context measure.
- Disability interpretation: Disability rate is included as a county-level access-support context measure. It does not identify postpartum disability or pregnancy-related disability.
- Legacy/general field note: The current ACS output may still contain `population_65_plus_rate`, but population age 65+ is not used for the planned postpartum index or planned Power BI pages.
- Limitation: ACS estimates are survey-based and county-level indicators may hide substantial within-county variation. Female population ages 15-44 is a proxy for reproductive-age population context; it does not directly identify postpartum Medicaid enrollees, pregnancy status, births, or postpartum coverage status.
- Status: Added by `scripts/05_add_acs_access_indicators.py`

## D. CMS Medicaid Enrollment

- Source: Medicaid.gov or CMS Medicaid/CHIP enrollment data
- Purpose: Optional state-level Medicaid enrollment context for interpreting the broader program environment.
- Note: State-level Medicaid enrollment may provide context but does not directly identify postpartum Medicaid enrollees. County-level Medicaid enrollment may not be consistently available nationally, and CMS enrollment data are not needed for the first county-level index.
- Status: Not added yet; optional state-level context only

## E. Rural-Urban Classification

- Source: NCHS 2023 Urban-Rural Classification Scheme for Counties
- Source page: `https://www.cdc.gov/nchs/data-analysis-tools/urban-rural.html`
- Source file: `https://www.cdc.gov/nchs/data/data-analysis/NCHSurb-rural-codes.csv`
- Purpose: Compare Medicaid office access patterns by urban-rural county type.
- Fields added: `nchs_urban_rural_code`, `nchs_urban_rural_category`, and `metro_nonmetro_flag`.
- Categories: Large central metro, large fringe metro, medium metro, small metro, micropolitan, and noncore.
- Limitation: County-level rurality may hide within-county variation, especially in large rural counties and mixed urban-suburban counties.
- Status: Added by `scripts/06_add_rural_urban_classification.py`

## F. Optional Social Vulnerability Index

- Source: CDC/ATSDR SVI
- Purpose: Deferred comparison or context layer.
- Note: SVI is not included in the first version of the Potential Postpartum Medicaid Administrative Access Barrier Index because the project already uses transparent ACS-derived indicators for poverty, transportation access, disability, language access, age, and race/ethnicity context. SVI may be added later as a comparison/context layer. Including SVI and its component-like ACS measures in the same index could overweight similar vulnerability domains.
- Status: Deferred; not included in first index version

## G. Hospital-Based Obstetric Care Status

- Source: University of Minnesota Rural Health Research Center / Rural Maternal Health Data Support and Analysis Program
- Dataset: 2010-2024 County-Level Hospital-Based Obstetric Care Status
- Source page: `https://rhrc.umn.edu/publication/2010-2024-county-level-hospital-based-obstetric-care-status/`
- Source file: `https://rhrc.umn.edu/wp-content/uploads/2026/05/county_OBstat_2010_2024.xlsx`
- Purpose: Identify whether counties have hospital-based obstetric care available.
- Use in project: Postpartum-specific clinical maternity access context that is distinct from Medicaid administrative and enrollment support access measured by office availability.
- Limitation: This identifies hospital-based obstetric care status, not all prenatal care, postpartum care, outpatient OB/GYN access, birth centers, doulas, midwives, community health centers, or Medicaid enrollment support.
- Status: Added by `scripts/07_add_obstetric_care_status.py`
