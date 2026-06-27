"""Build the county-level postpartum Medicaid access barrier index.

Inputs:
    data/processed/county_postpartum_access_analytic_base.csv

Outputs:
    data/processed/county_postpartum_access_index.csv
    data/processed/state_postpartum_access_index_summary.csv
    outputs/postpartum_access_barrier_index_summary.md

This step builds a transparent screening index from existing sourced layers.
It does not add new data sources, Power BI files, or raw data changes.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "county_postpartum_access_analytic_base.csv"
COUNTY_OUTPUT = PROJECT_ROOT / "data" / "processed" / "county_postpartum_access_index.csv"
STATE_OUTPUT = PROJECT_ROOT / "data" / "processed" / "state_postpartum_access_index_summary.csv"
SUMMARY_OUTPUT = PROJECT_ROOT / "outputs" / "postpartum_access_barrier_index_summary.md"

ANALYTIC_UNIVERSE = "50 states and District of Columbia"

HIGH_RATE_FIELDS = {
    "poverty_rate": "high_poverty_flag",
    "no_vehicle_rate": "high_no_vehicle_flag",
    "no_internet_rate": "high_no_internet_flag",
    "limited_english_rate": "high_limited_english_flag",
    "disability_rate": "high_disability_flag",
    "female_15_44_rate": "high_female_15_44_flag",
}

FLAG_LABELS = {
    "no_medicaid_office_flag": "No Medicaid office",
    "no_hospital_obstetric_care_flag": "No hospital-based obstetric care",
    "high_poverty_flag": "High poverty",
    "high_no_vehicle_flag": "High no-vehicle households",
    "high_no_internet_flag": "High no-internet subscription",
    "high_limited_english_flag": "High limited English",
    "high_disability_flag": "High disability",
    "high_female_15_44_flag": "High female population ages 15-44",
    "nonmetro_flag": "Nonmetro",
}

FLAG_WEIGHTS = {
    "no_medicaid_office_flag": 2,
    "no_hospital_obstetric_care_flag": 2,
    "high_poverty_flag": 1,
    "high_no_vehicle_flag": 1,
    "high_no_internet_flag": 1,
    "high_limited_english_flag": 1,
    "high_disability_flag": 1,
    "high_female_15_44_flag": 1,
    "nonmetro_flag": 1,
}

FLAG_FIELDS = list(FLAG_WEIGHTS)
EXCLUDED_OUTPUT_FIELDS = {"population_65_plus", "population_65_plus_rate"}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Required input file not found: {path}")
    with path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def require_fields(rows: list[dict[str, str]], fields: list[str]) -> None:
    if not rows:
        raise ValueError(f"Input file is empty: {INPUT_FILE}")
    available = set(rows[0])
    missing = sorted(set(fields) - available)
    if missing:
        raise ValueError("Input file is missing required fields: " + ", ".join(missing))


def to_float(value: str | None, *, field: str, county_fips: str) -> float:
    if value in {None, ""}:
        raise ValueError(f"Missing numeric value for {field} in county {county_fips}")
    try:
        return float(value)
    except ValueError as error:
        raise ValueError(
            f"Invalid numeric value {value!r} for {field} in county {county_fips}"
        ) from error


def to_int(value: str | None, *, field: str, county_fips: str) -> int:
    number = to_float(value, field=field, county_fips=county_fips)
    if number not in {0.0, 1.0}:
        raise ValueError(f"Expected 0/1 value for {field} in county {county_fips}: {value!r}")
    return int(number)


def percentile(values: list[float], percentile_value: float) -> float:
    """Return a linear-interpolated percentile using sorted values."""
    if not values:
        raise ValueError("Cannot calculate percentile for an empty value list")
    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * percentile_value
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = position - lower_index
    return sorted_values[lower_index] + (
        sorted_values[upper_index] - sorted_values[lower_index]
    ) * weight


def concern_level(score: int) -> str:
    if 0 <= score <= 2:
        return "Lower concern"
    if 3 <= score <= 5:
        return "Moderate concern"
    if 6 <= score <= 8:
        return "High concern"
    if 9 <= score <= 11:
        return "Highest concern"
    raise ValueError(f"Index score outside expected 0-11 range: {score}")


def calculate_thresholds(rows: list[dict[str, str]]) -> dict[str, float]:
    thresholds = {}
    for field in HIGH_RATE_FIELDS:
        values = [
            to_float(row.get(field), field=field, county_fips=row.get("county_fips", ""))
            for row in rows
        ]
        thresholds[field] = round(percentile(values, 0.75), 6)
    return thresholds


def build_county_index_rows(
    rows: list[dict[str, str]], thresholds: dict[str, float]
) -> list[dict[str, Any]]:
    indexed_rows: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda item: item["county_fips"]):
        county_fips = row["county_fips"]
        flags = {
            "no_medicaid_office_flag": 1
            if to_int(row.get("has_medicaid_office"), field="has_medicaid_office", county_fips=county_fips)
            == 0
            else 0,
            "no_hospital_obstetric_care_flag": to_int(
                row.get("no_hospital_obstetric_care"),
                field="no_hospital_obstetric_care",
                county_fips=county_fips,
            ),
            "nonmetro_flag": 1 if row.get("metro_nonmetro_flag") == "Nonmetro" else 0,
        }
        for rate_field, flag_field in HIGH_RATE_FIELDS.items():
            rate_value = to_float(row.get(rate_field), field=rate_field, county_fips=county_fips)
            flags[flag_field] = 1 if rate_value >= thresholds[rate_field] else 0

        score = sum(flags[field] * FLAG_WEIGHTS[field] for field in FLAG_FIELDS)
        triggered_labels = [FLAG_LABELS[field] for field in FLAG_FIELDS if flags[field] == 1]
        index_row = {
            key: value
            for key, value in row.items()
            if key not in EXCLUDED_OUTPUT_FIELDS
        }
        index_row.update(flags)
        index_row["index_component_count"] = sum(flags.values())
        index_row["index_component_summary"] = (
            "; ".join(triggered_labels) if triggered_labels else "No index components triggered"
        )
        index_row["postpartum_access_barrier_score"] = score
        index_row["postpartum_access_barrier_level"] = concern_level(score)
        indexed_rows.append(index_row)
    return indexed_rows


def build_state_summary_rows(index_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    state_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in index_rows:
        state_rows[row["state_fips"]].append(row)

    output_rows = []
    for state_fips, rows in sorted(state_rows.items()):
        scores = [int(row["postpartum_access_barrier_score"]) for row in rows]
        levels = Counter(row["postpartum_access_barrier_level"] for row in rows)
        high_or_highest = levels["High concern"] + levels["Highest concern"]
        counties_with_both_gaps = sum(
            1
            for row in rows
            if int(row["no_medicaid_office_flag"]) == 1
            and int(row["no_hospital_obstetric_care_flag"]) == 1
        )
        output_rows.append(
            {
                "state_fips": state_fips,
                "state_abbr": rows[0].get("state_abbr", ""),
                "state_name": rows[0].get("state_name", ""),
                "total_counties": len(rows),
                "average_postpartum_access_barrier_score": round(sum(scores) / len(scores), 6),
                "median_postpartum_access_barrier_score": median(scores),
                "counties_lower_concern": levels["Lower concern"],
                "counties_moderate_concern": levels["Moderate concern"],
                "counties_high_concern": levels["High concern"],
                "counties_highest_concern": levels["Highest concern"],
                "share_counties_high_or_highest_concern": round(high_or_highest / len(rows), 6),
                "counties_no_medicaid_office": sum(
                    int(row["no_medicaid_office_flag"]) for row in rows
                ),
                "counties_no_hospital_obstetric_care": sum(
                    int(row["no_hospital_obstetric_care_flag"]) for row in rows
                ),
                "counties_with_both_admin_and_clinical_gaps": counties_with_both_gaps,
            }
        )
    return output_rows


def format_thresholds(thresholds: dict[str, float]) -> str:
    return "\n".join(
        f"- `{field}`: {value}" for field, value in sorted(thresholds.items())
    )


def format_counter(counter: Counter[str]) -> str:
    order = ["Lower concern", "Moderate concern", "High concern", "Highest concern"]
    return "\n".join(f"- {level}: {counter[level]}" for level in order)


def format_flag_counts(index_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"- `{field}`: {sum(int(row[field]) for row in index_rows)}"
        for field in FLAG_FIELDS
    )


def format_top_counties(index_rows: list[dict[str, Any]], limit: int = 25) -> str:
    top_rows = sorted(
        index_rows,
        key=lambda row: (
            int(row["postpartum_access_barrier_score"]),
            int(row["index_component_count"]),
            row["county_name"],
        ),
        reverse=True,
    )[:limit]
    return "\n".join(
        "- {county_name}, {state_abbr} (`{county_fips}`): score={score}, level={level}, "
        "components={components}".format(
            county_name=row["county_name"],
            state_abbr=row["state_abbr"],
            county_fips=row["county_fips"],
            score=row["postpartum_access_barrier_score"],
            level=row["postpartum_access_barrier_level"],
            components=row["index_component_summary"],
        )
        for row in top_rows
    )


def format_top_states(state_rows: list[dict[str, Any]], limit: int = 10) -> str:
    top_rows = sorted(
        state_rows,
        key=lambda row: (
            row["share_counties_high_or_highest_concern"],
            row["average_postpartum_access_barrier_score"],
            row["state_name"],
        ),
        reverse=True,
    )[:limit]
    return "\n".join(
        "- {state_name} ({state_abbr}): share={share}, high/highest counties={high_total}, "
        "avg score={average}".format(
            state_name=row["state_name"],
            state_abbr=row["state_abbr"],
            share=row["share_counties_high_or_highest_concern"],
            high_total=row["counties_high_concern"] + row["counties_highest_concern"],
            average=row["average_postpartum_access_barrier_score"],
        )
        for row in top_rows
    )


def write_summary(
    input_rows: list[dict[str, str]],
    index_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    thresholds: dict[str, float],
) -> None:
    SUMMARY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    scores = [int(row["postpartum_access_barrier_score"]) for row in index_rows]
    level_counts = Counter(row["postpartum_access_barrier_level"] for row in index_rows)
    state_count = len({row["state_fips"] for row in index_rows})
    run_time = datetime.now().astimezone().isoformat(timespec="seconds")
    summary = f"""# Postpartum Access Barrier Index Summary

- Input file: `{INPUT_FILE.relative_to(PROJECT_ROOT)}`
- County index output: `{COUNTY_OUTPUT.relative_to(PROJECT_ROOT)}`
- State summary output: `{STATE_OUTPUT.relative_to(PROJECT_ROOT)}`
- Analytic universe: {ANALYTIC_UNIVERSE}
- Counties: {len(input_rows)}
- States/DC represented: {state_count}
- Score range observed: {min(scores)}-{max(scores)}
- Date/time run: {run_time}

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

{format_counter(level_counts)}

## Top-Quartile Thresholds

Thresholds use the 75th percentile across the 50 states and D.C. county analytic universe. Counties with values greater than or equal to the threshold are flagged.

{format_thresholds(thresholds)}

## Component Flag Counts

{format_flag_counts(index_rows)}

## Top 25 Counties By Postpartum Access Barrier Score

{format_top_counties(index_rows)}

## Top 10 States By Share Of High/Highest Concern Counties

{format_top_states(state_rows)}

## Limitations

- The index is a screening tool, not a causal measure.
- It does not identify individual postpartum Medicaid enrollees.
- Medicaid office availability reflects administrative/enrollment support access, not clinical care.
- Hospital-based obstetric care status reflects county-level hospital-based obstetric care availability, not all prenatal, postpartum, outpatient OB/GYN, midwife, doula, FQHC, or community-based support.
- Female population ages 15-44 is a proxy for reproductive-age population context, not a direct measure of births, pregnancy, postpartum status, or Medicaid coverage.
- Disability rate is included as a county-level access-support context measure, not as a direct measure of postpartum disability or pregnancy-related disability.
- County-level indicators may hide within-county variation.
"""
    SUMMARY_OUTPUT.write_text(summary, encoding="utf-8")


def main() -> int:
    rows = read_csv_rows(INPUT_FILE)
    required_fields = [
        "county_fips",
        "county_name",
        "state_fips",
        "state_abbr",
        "state_name",
        "has_medicaid_office",
        "no_hospital_obstetric_care",
        "metro_nonmetro_flag",
        *HIGH_RATE_FIELDS.keys(),
    ]
    require_fields(rows, required_fields)
    thresholds = calculate_thresholds(rows)
    index_rows = build_county_index_rows(rows, thresholds)
    state_rows = build_state_summary_rows(index_rows)

    base_fields = [field for field in rows[0].keys() if field not in EXCLUDED_OUTPUT_FIELDS]
    county_fields = [
        *base_fields,
        *FLAG_FIELDS,
        "index_component_count",
        "index_component_summary",
        "postpartum_access_barrier_score",
        "postpartum_access_barrier_level",
    ]
    state_fields = [
        "state_fips",
        "state_abbr",
        "state_name",
        "total_counties",
        "average_postpartum_access_barrier_score",
        "median_postpartum_access_barrier_score",
        "counties_lower_concern",
        "counties_moderate_concern",
        "counties_high_concern",
        "counties_highest_concern",
        "share_counties_high_or_highest_concern",
        "counties_no_medicaid_office",
        "counties_no_hospital_obstetric_care",
        "counties_with_both_admin_and_clinical_gaps",
    ]
    write_csv_rows(COUNTY_OUTPUT, index_rows, county_fields)
    write_csv_rows(STATE_OUTPUT, state_rows, state_fields)
    write_summary(rows, index_rows, state_rows, thresholds)

    scores = [int(row["postpartum_access_barrier_score"]) for row in index_rows]
    level_counts = Counter(row["postpartum_access_barrier_level"] for row in index_rows)
    print(f"Input file: {INPUT_FILE.relative_to(PROJECT_ROOT)}")
    print(f"County index output: {COUNTY_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"State summary output: {STATE_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Analytic universe: {ANALYTIC_UNIVERSE}")
    print(f"Counties: {len(index_rows)}")
    print(f"States/DC represented: {len({row['state_fips'] for row in index_rows})}")
    print(f"Score range observed: {min(scores)}-{max(scores)}")
    print("Concern level counts:")
    for line in format_counter(level_counts).splitlines():
        print(line)
    print("Top-quartile thresholds:")
    for line in format_thresholds(thresholds).splitlines():
        print(line)
    print("Component flag counts:")
    for line in format_flag_counts(index_rows).splitlines():
        print(line)
    print(f"Wrote summary: {SUMMARY_OUTPUT.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
