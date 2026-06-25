# ACS Access Indicators Summary

Pending generation by `scripts/05_add_acs_access_indicators.py`.

This branch adds `female_15_44_count` and `female_15_44_rate` using ACS 5-year Census API table `B01001` Sex by Age variables. The Codex runtime does not have `CENSUS_API_KEY`, and the Census API currently requires a key in this environment. The prior local ACS output cache does not contain populated female ages 15-44 fields, so the script is expected to stop rather than silently reuse incomplete cached data.

Run locally with a Census API key:

```bash
export CENSUS_API_KEY="your_key_here"
python3 scripts/05_add_acs_access_indicators.py
```

Expected generated contents include ACS source and vintage, county match counts, missingness for `female_15_44_count` and `female_15_44_rate`, min/max checks for `female_15_44_rate`, and the top 10 counties by `female_15_44_rate`.
