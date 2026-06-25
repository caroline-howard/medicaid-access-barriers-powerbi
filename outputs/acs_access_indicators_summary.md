# ACS Access Indicators Summary

Pending generation by `scripts/05_add_acs_access_indicators.py`.

This environment did not have a `CENSUS_API_KEY` available, so the ACS Census API pull was not run during this PR. The script is designed to overwrite this file with the full validation summary after it successfully reads `data/processed/county_office_access_base.csv` and retrieves ACS county indicators.

Expected generated contents include ACS source and vintage, input and output files, county match counts, indicators added, missingness checks, derived-rate min/max checks, and top counties by selected access-barrier indicators.
