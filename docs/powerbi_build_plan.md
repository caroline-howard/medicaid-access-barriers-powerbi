# Power BI Build Plan

## 1. National Postpartum Medicaid Access Overview

- Map counties with and without Medicaid office availability across the United States.
- Show state-level office counts and county coverage measures in relation to postpartum-relevant access indicators.
- Include filters for state, region, rurality, and data source notes as available.

## 2. Administrative vs. Clinical Access

- Compare administrative access, measured by Medicaid office availability, with clinical maternity access context, measured by hospital-based obstetric care status.
- Show counties with no Medicaid office, no hospital-based obstetric care, or both.
- Include metro/nonmetro and state filters to support policy-facing screening.

## 3. County Access Gaps

- Map counties with zero or low Medicaid office availability.
- Display county-level access context such as poverty, no-vehicle households, internet subscription, limited English, disability, female population ages 15-44, rurality, and obstetric care status.
- Include ranked county tables and tooltip details.

## 4. Potential Postpartum Medicaid Administrative Access Barrier Index

- Present a transparent county-level screening index combining administrative access, clinical maternity access context, poverty, transportation barriers, digital access barriers, language access, disability access-support context, female population ages 15-44, and metro/nonmetro status.
- Categorize counties into planned concern levels: lower, moderate, high, and highest concern.
- Provide ranked county tables by potential postpartum administrative access barrier score, slicers, and explanatory tooltips for index components.

Planned index component flags for the page and tooltips:

- `no_medicaid_office_flag`
- `no_hospital_obstetric_care_flag`
- `high_poverty_flag`
- `high_no_vehicle_flag`
- `high_no_internet_flag`
- `high_limited_english_flag`
- `high_disability_flag`
- `high_female_15_44_flag`
- `nonmetro_flag`

Do not include `high_age_65_plus_flag` as an index component or planned tooltip flag.

## 5. State Comparison

- Allow comparison of two states.
- Compare office counts, county coverage, office density, and rural-urban distribution.
- Highlight counties where limited office access overlaps with postpartum-relevant need and administrative access barriers.

## 6. Data Notes and Limitations

- Document source dates, data coverage, and refresh assumptions.
- State limitations around causal interpretation, point-in-time office data, county-level aggregation, missing non-office enrollment supports, and the fact that the dashboard does not identify individual postpartum Medicaid enrollees.
- Note that female population ages 15-44 is a proxy for reproductive-age population context, not a direct measure of postpartum need.
- Explain that administrative access refers to Medicaid office availability, while clinical maternity access refers to hospital-based obstetric care status.
- Provide clear caveats for portfolio and policy-facing interpretation.
