# Run Pipeline

Run the data-processing scripts in this order:

1. `scripts/02_clean_medicaid_offices.py`
2. `scripts/03_assign_offices_to_counties.py`
3. `scripts/04_build_county_office_access_base.py`
4. `scripts/05_add_acs_access_indicators.py`
5. `scripts/06_add_rural_urban_classification.py`
6. `scripts/07_add_obstetric_care_status.py`

Processed CSV outputs are generated locally under `data/processed/` and are not committed to the repository. Validation summaries under `outputs/` are tracked when they are small and useful for documenting pipeline checks.
