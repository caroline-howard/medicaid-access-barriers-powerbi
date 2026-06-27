# Current Data Status

This table summarizes the first-version data layers currently represented in the pipeline. Generated CSV outputs are produced locally and ignored by Git.

| Data Layer | Status | Script | Output |
| --- | --- | --- | --- |
| Medicaid offices | Complete | `scripts/02_clean_medicaid_offices.py` | `data/processed/medicaid_offices_clean.csv` |
| County assignment | Complete | `scripts/03_assign_offices_to_counties.py` | `data/processed/medicaid_offices_with_county.csv` |
| County office base | Complete | `scripts/04_build_county_office_access_base.py` | `data/processed/county_office_access_base.csv` |
| ACS indicators | Complete | `scripts/05_add_acs_access_indicators.py` | `data/processed/county_office_access_with_acs.csv` |
| Rurality | Complete | `scripts/06_add_rural_urban_classification.py` | `data/processed/county_office_access_with_acs_rurality.csv` |
| Obstetric care status | Complete | `scripts/07_add_obstetric_care_status.py` | `data/processed/county_postpartum_access_analytic_base.csv` |
| Access barrier index | Complete | `scripts/08_build_postpartum_access_barrier_index.py` | `data/processed/county_postpartum_access_index.csv` |
| Power BI export | Not built yet | future `scripts/09_prepare_powerbi_export.py` | future output |

## Planned Index Context Notes

- Population age 65+ is not part of the planned postpartum index or dashboard context.
- Disability rate remains a planned scoring component as a county-level access-support context measure, not as a direct measure of postpartum disability or pregnancy-related disability.
- `female_15_44_rate` is the postpartum-relevant reproductive-age population proxy.
