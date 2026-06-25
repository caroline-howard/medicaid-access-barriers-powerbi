# ACS Access Indicators Summary

- ACS source: U.S. Census Bureau American Community Survey 5-year API
- ACS vintage/year: 2024
- ACS data retrieval mode: existing local ACS output filtered to analytic universe
- Analytic universe: 50 states and District of Columbia
- Territories excluded: Yes, because the Medicaid office dataset covers the 50 states and D.C.
- Input file: `data/processed/county_office_access_base.csv`
- ACS indicator output: `data/processed/acs_county_access_indicators.csv`
- Merged output: `data/processed/county_office_access_with_acs.csv`
- Counties in office access base: 3144
- Counties with ACS match: 3144
- Counties missing ACS match: 0
- Date/time run: 2026-06-25T14:40:29-04:00

## Indicators Added

- poverty_rate
- no_vehicle_rate
- no_internet_rate
- limited_english_rate
- population_65_plus_rate
- disability_rate
- race/ethnicity context rates

## Missingness By Indicator

- `county_fips`: 0
- `county_name`: 0
- `state_fips`: 0
- `state_abbr`: 0
- `acs_year`: 0
- `total_population`: 0
- `poverty_universe`: 0
- `poverty_count`: 0
- `poverty_rate`: 0
- `households_total`: 0
- `households_no_vehicle`: 0
- `no_vehicle_rate`: 0
- `internet_households_total`: 0
- `households_without_internet_subscription`: 0
- `no_internet_rate`: 0
- `limited_english_universe`: 0
- `limited_english_count`: 0
- `limited_english_rate`: 0
- `population_65_plus`: 0
- `population_65_plus_rate`: 0
- `disability_universe`: 0
- `disability_count`: 0
- `disability_rate`: 0
- `race_ethnicity_total`: 0
- `non_hispanic_white_count`: 0
- `non_hispanic_white_rate`: 0
- `non_hispanic_black_count`: 0
- `non_hispanic_black_rate`: 0
- `hispanic_count`: 0
- `hispanic_rate`: 0
- `non_hispanic_asian_count`: 0
- `non_hispanic_asian_rate`: 0
- `non_hispanic_aian_count`: 0
- `non_hispanic_aian_rate`: 0

## Derived Rate Min/Max Checks

- `poverty_rate`: min=0.014159, max=0.575693
- `no_vehicle_rate`: min=0.0, max=0.829332
- `no_internet_rate`: min=0.0, max=0.453734
- `limited_english_rate`: min=0.0, max=0.320144
- `population_65_plus_rate`: min=0.044672, max=0.818182
- `disability_rate`: min=0.017956, max=0.727273
- `non_hispanic_white_rate`: min=0.022856, max=1.0
- `non_hispanic_black_rate`: min=0.0, max=0.85924
- `hispanic_rate`: min=0.0, max=0.972013
- `non_hispanic_asian_rate`: min=0.0, max=0.416107
- `non_hispanic_aian_rate`: min=0.0, max=0.907865

## Top 10 Counties By Poverty Rate

- Oglala Lakota County (`46102`): 0.575693
- Todd County (`46121`): 0.484264
- Corson County (`46031`): 0.442476
- Sioux County (`38085`): 0.432905
- Jackson County (`46071`): 0.423598
- Mellette County (`46095`): 0.417373
- Dimmit County (`48127`): 0.411059
- Greene County (`01063`): 0.401388
- Lee County (`05077`): 0.39441
- McCreary County (`21147`): 0.388565

## Top 10 Counties By No-Vehicle Rate

- Kusilvak Census Area (`02158`): 0.829332
- New York County (`36061`): 0.780371
- Northwest Arctic Borough (`02188`): 0.646027
- Bronx County (`36005`): 0.610784
- Bethel Census Area (`02050`): 0.576636
- Kings County (`36047`): 0.563519
- Nome Census Area (`02180`): 0.558594
- Lake and Peninsula Borough (`02164`): 0.435185
- Queens County (`36081`): 0.374303
- North Slope Borough (`02185`): 0.370013

## Top 10 Counties By No-Internet Rate

- Claiborne Parish (`22027`): 0.453734
- Lunenburg County (`51111`): 0.368476
- Apache County (`04001`): 0.364076
- Pulaski County (`17153`): 0.362887
- Baker County (`13007`): 0.357401
- Alexander County (`17003`): 0.354517
- Holmes County (`39075`): 0.34916
- Mora County (`35033`): 0.340955
- Quitman County (`13239`): 0.330834
- Jasper County (`28061`): 0.327516

## Known Limitations

ACS estimates are survey-based and include uncertainty not represented in this first indicator file. County-level indicators may hide important within-county variation. Puerto Rico and other territories are excluded because the Medicaid office dataset covers the 50 states and D.C. This step adds contextual access-barrier indicators only; it does not calculate a barrier index or add CMS enrollment or rurality data.
