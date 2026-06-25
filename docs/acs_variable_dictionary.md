# ACS Variable Dictionary

This project uses ACS 5-year county-level variables from the most recent Census API vintage available at run time. See `scripts/05_add_acs_access_indicators.py` for the executable mapping.

| ACS endpoint | ACS table ID | ACS variable ID | Plain-English label | Derived field name | Calculation formula |
| --- | --- | --- | --- | --- | --- |
| ACS 5-year detail | B01003 | B01003_001E | Total population | total_population | Raw count |
| ACS 5-year detail | B17001 | B17001_001E | Poverty status universe | poverty_universe | Raw count |
| ACS 5-year detail | B17001 | B17001_002E | Population below poverty level | poverty_count | Raw count |
| ACS 5-year detail | B17001 | B17001_002E / B17001_001E | Poverty rate | poverty_rate | poverty_count / poverty_universe |
| ACS 5-year detail | B08201 | B08201_001E | Total households for vehicle availability | households_total | Raw count |
| ACS 5-year detail | B08201 | B08201_002E | Households with no vehicle available | households_no_vehicle | Raw count |
| ACS 5-year detail | B08201 | B08201_002E / B08201_001E | No-vehicle household rate | no_vehicle_rate | households_no_vehicle / households_total |
| ACS 5-year detail | B28002 | B28002_001E | Total households for internet subscription | internet_households_total | Raw count |
| ACS 5-year detail | B28002 | B28002_013E | Households without an internet subscription | households_without_internet_subscription | Raw count |
| ACS 5-year detail | B28002 | B28002_013E / B28002_001E | No internet subscription rate | no_internet_rate | households_without_internet_subscription / internet_households_total |
| ACS 5-year detail | C16002 | C16002_001E | Household language universe | limited_english_universe | Raw count |
| ACS 5-year detail | C16002 | C16002_004E + C16002_007E + C16002_010E + C16002_013E | Limited-English-speaking households | limited_english_count | Sum of limited-English household language categories |
| ACS 5-year detail | C16002 | limited_english_count / C16002_001E | Limited-English household rate | limited_english_rate | limited_english_count / limited_english_universe |
| ACS 5-year detail | B01001 | B01001_020E through B01001_025E plus B01001_044E through B01001_049E | Population age 65 and older | population_65_plus | Sum of male and female age 65+ categories |
| ACS 5-year detail | B01001 | population_65_plus / B01001_001E | Age 65+ population rate | population_65_plus_rate | population_65_plus / age_sex_total_population |
| ACS 5-year subject | S1810 | S1810_C01_001E | Civilian noninstitutionalized population | disability_universe | Raw count |
| ACS 5-year subject | S1810 | S1810_C02_001E | Civilian noninstitutionalized population with a disability | disability_count | Raw count |
| ACS 5-year subject | S1810 | S1810_C02_001E / S1810_C01_001E | Disability rate | disability_rate | disability_count / disability_universe |
| ACS 5-year detail | B03002 | B03002_001E | Hispanic or Latino origin by race universe | race_ethnicity_total | Raw count |
| ACS 5-year detail | B03002 | B03002_003E | Non-Hispanic White alone population | non_hispanic_white_count | Raw count |
| ACS 5-year detail | B03002 | B03002_003E / B03002_001E | Non-Hispanic White alone rate | non_hispanic_white_rate | non_hispanic_white_count / race_ethnicity_total |
| ACS 5-year detail | B03002 | B03002_004E | Non-Hispanic Black alone population | non_hispanic_black_count | Raw count |
| ACS 5-year detail | B03002 | B03002_004E / B03002_001E | Non-Hispanic Black alone rate | non_hispanic_black_rate | non_hispanic_black_count / race_ethnicity_total |
| ACS 5-year detail | B03002 | B03002_012E | Hispanic or Latino population | hispanic_count | Raw count |
| ACS 5-year detail | B03002 | B03002_012E / B03002_001E | Hispanic or Latino rate | hispanic_rate | hispanic_count / race_ethnicity_total |
| ACS 5-year detail | B03002 | B03002_006E | Non-Hispanic Asian alone population | non_hispanic_asian_count | Raw count |
| ACS 5-year detail | B03002 | B03002_006E / B03002_001E | Non-Hispanic Asian alone rate | non_hispanic_asian_rate | non_hispanic_asian_count / race_ethnicity_total |
| ACS 5-year detail | B03002 | B03002_005E | Non-Hispanic American Indian and Alaska Native alone population | non_hispanic_aian_count | Raw count |
| ACS 5-year detail | B03002 | B03002_005E / B03002_001E | Non-Hispanic American Indian and Alaska Native alone rate | non_hispanic_aian_rate | non_hispanic_aian_count / race_ethnicity_total |
