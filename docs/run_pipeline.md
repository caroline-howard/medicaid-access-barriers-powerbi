# Run Pipeline

## Prerequisites

- Run commands from the repository root.
- Save the raw Medicaid office Excel file as `data/raw/medicaid_offices.xlsx`.
- Set `CENSUS_API_KEY` before running the ACS script:

```bash
export CENSUS_API_KEY="your_key_here"
```

- Processed CSV outputs are generated locally under `data/processed/` and are ignored by Git.
- Validation summaries under `outputs/` are tracked when they are small and useful for documenting pipeline checks.

## Script Order

Run the data-processing scripts in this order:

1. `scripts/02_clean_medicaid_offices.py`
2. `scripts/03_assign_offices_to_counties.py`
3. `scripts/04_build_county_office_access_base.py`
4. `scripts/05_add_acs_access_indicators.py`
5. `scripts/06_add_rural_urban_classification.py`
6. `scripts/07_add_obstetric_care_status.py`
7. `scripts/08_build_postpartum_access_barrier_index.py`

The next planned step is preparing the Power BI export package.
