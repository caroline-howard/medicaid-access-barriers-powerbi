# Project Plan

## Project Purpose

This project will build a Power BI portfolio dashboard focused on postpartum Medicaid administrative access barriers. The dashboard combines public Medicaid office-location data, county-level ACS indicators, rural-urban context, and hospital-based obstetric care status to identify counties where limited office availability overlaps with postpartum-relevant access barriers after delivery.

The dashboard is intended as a policy-facing screening tool for identifying places that may warrant closer review, outreach, or support planning. It is not a causal analysis of Medicaid enrollment, retention, or health outcomes.

## Completed Milestones

- Medicaid office cleaning
- County assignment
- Complete county office access base table
- ACS indicators
- Female population ages 15-44
- Rural-urban classification
- Hospital-based obstetric care status

## Current Data Pipeline

1. Acquire the Medicaid office locations dataset from Harvard Dataverse.
2. Clean office address and coordinate fields.
3. Assign office points to counties.
4. Build a complete county office access base table, including zero-office counties.
5. Add ACS indicators relevant to postpartum administrative access barriers, including female population ages 15-44.
6. Add rural-urban classification to support metro/nonmetro comparisons.
7. Add hospital-based obstetric care status as clinical maternity access context.

## Future Milestones

- Build the Potential Postpartum Medicaid Administrative Access Barrier Index.
- Prepare Power BI export files.
- Build the Power BI report.
- Write portfolio summary.

## Planned Index Design

Medicaid office availability is an administrative and enrollment support access measure. Hospital-based obstetric care status is a clinical maternity access measure. Female population ages 15-44 is a reproductive-age population context proxy. Disability rate is included as an access-support context measure, not as a direct measure of postpartum disability or pregnancy-related disability.

Population age 65+ should not be used in the score or presented as a planned dashboard context measure because the project is focused on postpartum Medicaid access barriers.

Planned score components:

- No Medicaid office in county = 2 points
- No hospital-based obstetric care = 2 points
- Top quartile poverty rate = 1 point
- Top quartile no-vehicle household rate = 1 point
- Top quartile no-internet subscription rate = 1 point
- Top quartile limited English rate = 1 point
- Top quartile disability rate = 1 point
- Top quartile female population ages 15-44 rate = 1 point
- Nonmetro county = 1 point

Planned score range: 0-11 points

Planned concern levels:

- 0-2 = Lower concern
- 3-5 = Moderate concern
- 6-8 = High concern
- 9-11 = Highest concern

## Planned Power BI Outputs

- National Postpartum Medicaid Access Overview
- Administrative vs. Clinical Access page
- State comparison dashboard page
- County access gaps page
- Potential Postpartum Medicaid Administrative Access Barrier Index page
- Data notes and limitations page

## Current Milestone Note

This cleanup milestone is limited to documentation, repo organization, pipeline instructions, status labels, and validation summary review. It does not add new data sources, Power BI files, or index calculations.
