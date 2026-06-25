# Obstetric Care Status Summary

- Source: University of Minnesota Rural Health Research Center / Rural Maternal Health Data Support and Analysis Program
- Dataset: 2010-2024 County-Level Hospital-Based Obstetric Care Status
- Source page: https://rhrc.umn.edu/publication/2010-2024-county-level-hospital-based-obstetric-care-status/
- Source file: https://rhrc.umn.edu/wp-content/uploads/2026/05/county_OBstat_2010_2024.xlsx
- Current obstetric care year used: 2024
- Analytic universe: 50 states and District of Columbia
- Input file: `data/processed/county_office_access_with_acs_rurality.csv`
- Obstetric care output: `data/processed/hospital_obstetric_care_status.csv`
- Merged analytic output: `data/processed/county_postpartum_access_analytic_base.csv`
- Counties in input analytic file: 3144
- Counties with obstetric care status match: 3144
- Counties missing obstetric care status: 0
- States/DC represented: 51
- Counties with hospital-based obstetric care: 1484
- Counties without hospital-based obstetric care: 1660
- Share of counties without hospital-based obstetric care: 0.52799
- Date/time run: 2026-06-25T15:11:33-04:00

## Metro/Nonmetro Summary

- Metro: 1186 counties, 723 with care, 463 without care, 0.390388 share without care
- Nonmetro: 1958 counties, 761 with care, 1197 without care, 0.611338 share without care

## Medicaid Office Availability Summary

- 0: 733 counties, 155 with care, 578 without care, 0.78854 share without care
- 1: 2411 counties, 1329 with care, 1082 without care, 0.448776 share without care

## Notes on Limitations

This dataset identifies whether hospital-based obstetric care was available in each county and year. It does not capture all prenatal care, postpartum care, outpatient OB/GYN access, birth centers, doulas, midwives, community health centers, Medicaid enrollment support, or cross-county care seeking. This step adds clinical access context only and does not calculate the Potential Postpartum Medicaid Administrative Access Barrier Index.
