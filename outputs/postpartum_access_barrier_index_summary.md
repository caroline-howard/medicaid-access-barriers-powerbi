# Postpartum Access Barrier Index Summary

- Input file: `data/processed/county_postpartum_access_analytic_base.csv`
- County index output: `data/processed/county_postpartum_access_index.csv`
- State summary output: `data/processed/state_postpartum_access_index_summary.csv`
- Analytic universe: 50 states and District of Columbia
- Counties: 3144
- States/DC represented: 51
- Score range observed: 0-10
- Date/time run: 2026-06-27T18:42:44-04:00

## Score Design

- No Medicaid office in county: 2 points
- No hospital-based obstetric care: 2 points
- Top quartile poverty rate: 1 point
- Top quartile no-vehicle household rate: 1 point
- Top quartile no-internet subscription rate: 1 point
- Top quartile limited English rate: 1 point
- Top quartile disability rate: 1 point
- Top quartile female population ages 15-44 rate: 1 point
- Nonmetro county: 1 point

Population age 65+ is not used in the score, and no `high_age_65_plus_flag` is created.

## Concern Level Counts

- Lower concern: 1070
- Moderate concern: 1409
- High concern: 609
- Highest concern: 56

## Top-Quartile Thresholds

Thresholds use the 75th percentile across the 50 states and D.C. county analytic universe. Counties with values greater than or equal to the threshold are flagged.

- `disability_rate`: 0.190655
- `female_15_44_rate`: 0.190378
- `limited_english_rate`: 0.019889
- `no_internet_rate`: 0.13514
- `no_vehicle_rate`: 0.07088
- `poverty_rate`: 0.173449

## Component Flag Counts

- `no_medicaid_office_flag`: 733
- `no_hospital_obstetric_care_flag`: 1660
- `high_poverty_flag`: 786
- `high_no_vehicle_flag`: 786
- `high_no_internet_flag`: 786
- `high_limited_english_flag`: 786
- `high_disability_flag`: 786
- `high_female_15_44_flag`: 786
- `nonmetro_flag`: 1958

## Top 25 Counties By Postpartum Access Barrier Score

- Tillman County, OK (`40141`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High limited English; High disability; Nonmetro
- Sumter County, AL (`01119`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44; Nonmetro
- Perry County, AL (`01105`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44; Nonmetro
- Noxubee County, MS (`28103`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44; Nonmetro
- Madison Parish, LA (`22065`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44; Nonmetro
- Humphreys County, MS (`28053`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44; Nonmetro
- Harmon County, OK (`40057`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High limited English; High disability; Nonmetro
- Harding County, NM (`35021`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High limited English; High disability; Nonmetro
- Evangeline Parish, LA (`22039`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44; Nonmetro
- Duval County, TX (`48131`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High limited English; High disability; Nonmetro
- Barbour County, AL (`01005`): score=10, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High limited English; High disability; Nonmetro
- Dimmit County, TX (`48127`): score=9, level=Highest concern, components=No Medicaid office; High poverty; High no-vehicle households; High no-internet subscription; High limited English; High disability; High female population ages 15-44; Nonmetro
- Winston County, MS (`28159`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro
- Winn Parish, LA (`22127`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro
- Wilkinson County, MS (`28157`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro
- Wilcox County, AL (`01131`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro
- Tishomingo County, MS (`28141`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-internet subscription; High limited English; High disability; Nonmetro
- Tensas Parish, LA (`22107`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro
- St. Helena Parish, LA (`22091`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44
- Skagway Municipality, AK (`02230`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High no-vehicle households; High limited English; High disability; High female population ages 15-44; Nonmetro
- Sharkey County, MS (`28125`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High female population ages 15-44; Nonmetro
- San Augustine County, TX (`48405`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro
- Sabine Parish, LA (`22085`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro
- Russell County, AL (`01113`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; High female population ages 15-44
- Red River Parish, LA (`22081`): score=9, level=Highest concern, components=No Medicaid office; No hospital-based obstetric care; High poverty; High no-vehicle households; High no-internet subscription; High disability; Nonmetro

## Top 10 States By Share Of High/Highest Concern Counties

- Mississippi (MS): share=0.658537, high/highest counties=54, avg score=6.134146
- Alaska (AK): share=0.6, high/highest counties=18, avg score=5.5
- Louisiana (LA): share=0.5625, high/highest counties=36, avg score=6.015625
- Alabama (AL): share=0.552239, high/highest counties=37, avg score=5.671642
- Oklahoma (OK): share=0.519481, high/highest counties=40, avg score=5.285714
- New Mexico (NM): share=0.484848, high/highest counties=16, avg score=5.515152
- Arkansas (AR): share=0.36, high/highest counties=27, avg score=4.746667
- Texas (TX): share=0.350394, high/highest counties=89, avg score=4.586614
- West Virginia (WV): share=0.327273, high/highest counties=18, avg score=4.236364
- Idaho (ID): share=0.318182, high/highest counties=14, avg score=4.045455

## Limitations

- The index is a screening tool, not a causal measure.
- It does not identify individual postpartum Medicaid enrollees.
- Medicaid office availability reflects administrative/enrollment support access, not clinical care.
- Hospital-based obstetric care status reflects county-level hospital-based obstetric care availability, not all prenatal, postpartum, outpatient OB/GYN, midwife, doula, FQHC, or community-based support.
- Female population ages 15-44 is a proxy for reproductive-age population context, not a direct measure of births, pregnancy, postpartum status, or Medicaid coverage.
- Disability rate is included as a county-level access-support context measure, not as a direct measure of postpartum disability or pregnancy-related disability.
- County-level indicators may hide within-county variation.
