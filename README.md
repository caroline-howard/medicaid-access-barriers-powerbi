# Medicaid Access Barriers Power BI Dashboard

Power BI portfolio project analyzing geographic access to Medicaid office locations and county-level administrative access barriers using public health, demographic, and spatial data.

## Main Research Question

Where may in-person Medicaid enrollment support be limited relative to population need, transportation barriers, and digital access constraints?

## Planned Data Sources

- Shafer et al. 2024 geocoded Medicaid office locations dataset from Harvard Dataverse
- Census or ACS county-level demographic indicators
- CMS Medicaid enrollment data
- Rural-urban classification data
- Optional CDC/ATSDR Social Vulnerability Index

## Planned Power BI Report Pages

1. National Medicaid Office Access Map
2. State Comparison
3. County Access Gaps
4. Access Barrier Index
5. Data Notes and Limitations

## Current Project Status

Initial repository setup. This project currently contains the planned folder structure and documentation placeholders only. Data acquisition, cleaning, spatial joins, index development, and Power BI report construction have not started yet.

## Data Source Setup

The primary data source is the Shafer et al. 2024 geocoded Medicaid office locations dataset from Harvard Dataverse. The raw Excel file should be saved locally as `data/raw/medicaid_offices.xlsx`.

Raw data should remain unchanged. Cleaning, county spatial joins, access-barrier measures, and export-ready tables will be handled in later scripts. This setup step does not perform analysis yet.

## Current Data Pipeline

1. Raw Medicaid office Excel file: `data/raw/medicaid_offices.xlsx`
2. Clean Medicaid office CSV: `data/processed/medicaid_offices_clean.csv`
3. County-assigned office file: `data/processed/medicaid_offices_with_county.csv`
4. Complete county office access base table: `data/processed/county_office_access_base.csv`
5. Future step: add ACS/access-barrier indicators
6. Future step: add rural-urban classification
7. Future step: build access-barrier index
8. Future step: build Power BI report

## Notes on Limitations

- The project will identify potential geographic and administrative access barriers; it will not claim that office availability causes Medicaid enrollment outcomes.
- The Medicaid office dataset is a point-in-time public dataset and should not be presented as a live office locator.
- County-level indicators may hide important within-county variation, especially in large rural counties and dense urban counties.
- The first project milestone does not include raw data files, processed datasets, or analytic outputs.
