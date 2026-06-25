# Data Download Instructions

## Medicaid Office Locations

The primary raw data file for this project is the Shafer et al. 2024 geocoded Medicaid office locations dataset from Harvard Dataverse.

1. Go to Harvard Dataverse.
2. Search for the dataset DOI: `10.7910/DVN/AVRHMI`.
3. Open the dataset page for "A dataset of geocoded Medicaid office locations in the United States."
4. Download the Excel version of the office locations dataset.
5. Save the file as `data/raw/medicaid_offices.xlsx`.
6. Do not rename columns manually.
7. Do not edit the raw file.

## Why Raw Data Should Stay Unchanged

Raw files should be preserved exactly as downloaded so the project remains reproducible. Any renaming, filtering, cleaning, spatial joins, or derived indicators should be handled in scripts and saved to `data/processed/` in later milestones.
