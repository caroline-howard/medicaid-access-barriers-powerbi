# Postpartum Medicaid Access Barriers Power BI Dashboard

Power BI portfolio project identifying where postpartum Medicaid populations may face greater administrative access barriers after delivery using geocoded Medicaid office locations, county-level demographic and access indicators, and spatial context.

## Main Research Question

Where may postpartum Medicaid populations face greater administrative access barriers to maintaining coverage and navigating support after delivery?

## Project Purpose

This project uses geocoded Medicaid office locations, county-level ACS indicators, and rural-urban context to identify counties where limited office availability overlaps with postpartum-relevant access barriers.

The goal is to support a policy-facing screening dashboard for identifying places that may warrant closer review, outreach, or support planning. It is not designed as a causal analysis of Medicaid enrollment, retention, or health outcomes.

## Planned Data Sources

- Shafer et al. 2024 geocoded Medicaid office locations dataset from Harvard Dataverse
- Census or ACS county-level demographic indicators
- Hospital-based obstetric care status
- CMS Medicaid enrollment data
- Rural-urban classification data
- Optional CDC/ATSDR Social Vulnerability Index

## Planned Power BI Report Pages

1. National Postpartum Medicaid Access Overview
2. State Comparison
3. County Access Gaps
4. Potential Postpartum Medicaid Administrative Access Barrier Index
5. Data Notes and Limitations

## Planned Potential Postpartum Medicaid Administrative Access Barrier Index

Planned index components include:

- No Medicaid office in county
- Poverty rate
- No vehicle household rate
- No internet subscription rate
- Limited English rate
- Disability rate
- No hospital-based obstetric care identified
- Female population ages 15-44, to be added in a future ACS update
- Rural/nonmetro status, to be added through rural-urban classification

## Current Project Status

Initial data-processing scaffolding is underway. Current project framing is being narrowed around postpartum Medicaid administrative access barriers. Index development and Power BI report construction have not started yet.

## Data Source Setup

The primary data source is the Shafer et al. 2024 geocoded Medicaid office locations dataset from Harvard Dataverse. The raw Excel file should be saved locally as `data/raw/medicaid_offices.xlsx`.

Raw data should remain unchanged. Cleaning, county spatial joins, postpartum-relevant access-barrier measures, and export-ready tables will be handled by scripts. This documentation step does not add new data or perform index calculations.

## Current Data Pipeline

1. Raw Medicaid office Excel file: `data/raw/medicaid_offices.xlsx`
2. County office access base: `data/processed/county_office_access_base.csv`
3. ACS access-barrier indicators: `data/processed/acs_county_access_indicators.csv`
4. Rural-urban classification: `data/processed/county_office_access_with_acs_rurality.csv`
5. Hospital-based obstetric care status: `data/processed/county_postpartum_access_analytic_base.csv`
6. Future step: build Potential Postpartum Medicaid Administrative Access Barrier Index
7. Future step: build Power BI report

## Notes on Limitations

- The dashboard does not identify individual postpartum Medicaid enrollees.
- The Potential Postpartum Medicaid Administrative Access Barrier Index is a screening tool, not a causal measure.
- The project will identify potential geographic and administrative access barriers; it will not claim that office availability causes Medicaid enrollment, retention, or health outcomes.
- The Medicaid office dataset is a point-in-time public dataset and should not be presented as a live office locator.
- County-level indicators may hide important within-county variation, especially in large rural counties and dense urban counties.
- Medicaid office availability does not capture all enrollment assistance, online support, navigators, health systems, or community-based support.
- Female population ages 15-44 is a proxy for reproductive-age population context, not a direct measure of postpartum need.
- Raw and processed datasets are generated or stored locally and are not committed to the repository.
