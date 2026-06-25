"""Add ACS county-level access-barrier indicators.

Inputs:
    data/processed/county_office_access_base.csv

Outputs:
    data/processed/acs_county_access_indicators.csv
    data/processed/county_office_access_with_acs.csv
    outputs/acs_access_indicators_summary.md

This step adds ACS county indicators only. It does not add CMS enrollment,
rurality, Power BI files, or access-barrier index calculations.

Set CENSUS_API_KEY in the environment before running if the Census API requires
a key in your environment.
"""

from __future__ import annotations

import csv
import json
import os
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COUNTY_BASE_INPUT = PROJECT_ROOT / "data" / "processed" / "county_office_access_base.csv"
ACS_OUTPUT = PROJECT_ROOT / "data" / "processed" / "acs_county_access_indicators.csv"
MERGED_OUTPUT = PROJECT_ROOT / "data" / "processed" / "county_office_access_with_acs.csv"
SUMMARY_OUTPUT = PROJECT_ROOT / "outputs" / "acs_access_indicators_summary.md"

DETAIL_ENDPOINT = "acs/acs5"
SUBJECT_ENDPOINT = "acs/acs5/subject"
START_YEAR = datetime.now().year - 1
EARLIEST_YEAR = 2020

RAW_VARIABLES: OrderedDict[str, tuple[str, str, str]] = OrderedDict(
    [
        ("total_population", (DETAIL_ENDPOINT, "B01003", "B01003_001E")),
        ("poverty_universe", (DETAIL_ENDPOINT, "B17001", "B17001_001E")),
        ("poverty_count", (DETAIL_ENDPOINT, "B17001", "B17001_002E")),
        ("households_total", (DETAIL_ENDPOINT, "B08201", "B08201_001E")),
        ("households_no_vehicle", (DETAIL_ENDPOINT, "B08201", "B08201_002E")),
        ("internet_households_total", (DETAIL_ENDPOINT, "B28002", "B28002_001E")),
        (
            "households_without_internet_subscription",
            (DETAIL_ENDPOINT, "B28002", "B28002_013E"),
        ),
        ("limited_english_universe", (DETAIL_ENDPOINT, "C16002", "C16002_001E")),
        ("limited_english_spanish", (DETAIL_ENDPOINT, "C16002", "C16002_004E")),
        (
            "limited_english_other_indo_european",
            (DETAIL_ENDPOINT, "C16002", "C16002_007E"),
        ),
        (
            "limited_english_asian_pacific_island",
            (DETAIL_ENDPOINT, "C16002", "C16002_010E"),
        ),
        ("limited_english_other_language", (DETAIL_ENDPOINT, "C16002", "C16002_013E")),
        ("age_sex_total_population", (DETAIL_ENDPOINT, "B01001", "B01001_001E")),
        ("male_65_66", (DETAIL_ENDPOINT, "B01001", "B01001_020E")),
        ("male_67_69", (DETAIL_ENDPOINT, "B01001", "B01001_021E")),
        ("male_70_74", (DETAIL_ENDPOINT, "B01001", "B01001_022E")),
        ("male_75_79", (DETAIL_ENDPOINT, "B01001", "B01001_023E")),
        ("male_80_84", (DETAIL_ENDPOINT, "B01001", "B01001_024E")),
        ("male_85_plus", (DETAIL_ENDPOINT, "B01001", "B01001_025E")),
        ("female_65_66", (DETAIL_ENDPOINT, "B01001", "B01001_044E")),
        ("female_67_69", (DETAIL_ENDPOINT, "B01001", "B01001_045E")),
        ("female_70_74", (DETAIL_ENDPOINT, "B01001", "B01001_046E")),
        ("female_75_79", (DETAIL_ENDPOINT, "B01001", "B01001_047E")),
        ("female_80_84", (DETAIL_ENDPOINT, "B01001", "B01001_048E")),
        ("female_85_plus", (DETAIL_ENDPOINT, "B01001", "B01001_049E")),
        ("race_ethnicity_total", (DETAIL_ENDPOINT, "B03002", "B03002_001E")),
        ("non_hispanic_white_count", (DETAIL_ENDPOINT, "B03002", "B03002_003E")),
        ("non_hispanic_black_count", (DETAIL_ENDPOINT, "B03002", "B03002_004E")),
        ("non_hispanic_aian_count", (DETAIL_ENDPOINT, "B03002", "B03002_005E")),
        ("non_hispanic_asian_count", (DETAIL_ENDPOINT, "B03002", "B03002_006E")),
        ("hispanic_count", (DETAIL_ENDPOINT, "B03002", "B03002_012E")),
        ("disability_universe", (SUBJECT_ENDPOINT, "S1810", "S1810_C01_001E")),
        ("disability_count", (SUBJECT_ENDPOINT, "S1810", "S1810_C02_001E")),
    ]
)

ACS_OUTPUT_FIELDS = [
    "county_fips",
    "county_name",
    "state_fips",
    "state_abbr",
    "acs_year",
    "total_population",
    "poverty_universe",
    "poverty_count",
    "poverty_rate",
    "households_total",
    "households_no_vehicle",
    "no_vehicle_rate",
    "internet_households_total",
    "households_without_internet_subscription",
    "no_internet_rate",
    "limited_english_universe",
    "limited_english_count",
    "limited_english_rate",
    "population_65_plus",
    "population_65_plus_rate",
    "disability_universe",
    "disability_count",
    "disability_rate",
    "race_ethnicity_total",
    "non_hispanic_white_count",
    "non_hispanic_white_rate",
    "non_hispanic_black_count",
    "non_hispanic_black_rate",
    "hispanic_count",
    "hispanic_rate",
    "non_hispanic_asian_count",
    "non_hispanic_asian_rate",
    "non_hispanic_aian_count",
    "non_hispanic_aian_rate",
]

RATE_FIELDS = [
    "poverty_rate",
    "no_vehicle_rate",
    "no_internet_rate",
    "limited_english_rate",
    "population_65_plus_rate",
    "disability_rate",
    "non_hispanic_white_rate",
    "non_hispanic_black_rate",
    "hispanic_rate",
    "non_hispanic_asian_rate",
    "non_hispanic_aian_rate",
]

STATE_FIPS_TO_ABBR = {
    "01": "AL",
    "02": "AK",
    "04": "AZ",
    "05": "AR",
    "06": "CA",
    "08": "CO",
    "09": "CT",
    "10": "DE",
    "11": "DC",
    "12": "FL",
    "13": "GA",
    "15": "HI",
    "16": "ID",
    "17": "IL",
    "18": "IN",
    "19": "IA",
    "20": "KS",
    "21": "KY",
    "22": "LA",
    "23": "ME",
    "24": "MD",
    "25": "MA",
    "26": "MI",
    "27": "MN",
    "28": "MS",
    "29": "MO",
    "30": "MT",
    "31": "NE",
    "32": "NV",
    "33": "NH",
    "34": "NJ",
    "35": "NM",
    "36": "NY",
    "37": "NC",
    "38": "ND",
    "39": "OH",
    "40": "OK",
    "41": "OR",
    "42": "PA",
    "44": "RI",
    "45": "SC",
    "46": "SD",
    "47": "TN",
    "48": "TX",
    "49": "UT",
    "50": "VT",
    "51": "VA",
    "53": "WA",
    "54": "WV",
    "55": "WI",
    "56": "WY",
    "60": "AS",
    "66": "GU",
    "69": "MP",
    "72": "PR",
    "78": "VI",
}


def get_api_key() -> str:
    key = os.environ.get("CENSUS_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "CENSUS_API_KEY is not set. The Census API requires a key in this "
            "environment; set CENSUS_API_KEY and rerun this script."
        )
    return key


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise RuntimeError(
            f"Missing expected input: {path.relative_to(PROJECT_ROOT)}. "
            "Build the county office access base table before adding ACS indicators."
        )
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fetch_json(url: str) -> list[list[str]]:
    try:
        with urlopen(url, timeout=60) as response:
            text = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Census API request failed: {exc}") from exc

    if text.lstrip().startswith("<"):
        raise RuntimeError(f"Census API returned HTML instead of JSON: {text[:160]}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Census API returned invalid JSON: {exc}") from exc


def variable_ids_for_endpoint(endpoint: str) -> list[str]:
    return [
        variable_id
        for _, (variable_endpoint, _, variable_id) in RAW_VARIABLES.items()
        if variable_endpoint == endpoint
    ]


def fetch_endpoint_data(year: int, endpoint: str, api_key: str) -> dict[str, dict[str, str]]:
    variable_ids = variable_ids_for_endpoint(endpoint)
    params = {
        "get": ",".join(["NAME", *variable_ids]),
        "for": "county:*",
        "in": "state:*",
        "key": api_key,
    }
    url = f"https://api.census.gov/data/{year}/{endpoint}?{urlencode(params)}"
    data = fetch_json(url)
    headers = data[0]
    rows = data[1:]

    output: dict[str, dict[str, str]] = {}
    for values in rows:
        record = dict(zip(headers, values, strict=True))
        county_fips = f"{record['state']}{record['county']}"
        output[county_fips] = record
    return output


def discover_acs_year(api_key: str) -> int:
    for year in range(START_YEAR, EARLIEST_YEAR - 1, -1):
        try:
            fetch_endpoint_data(year, DETAIL_ENDPOINT, api_key)
            fetch_endpoint_data(year, SUBJECT_ENDPOINT, api_key)
            return year
        except RuntimeError:
            continue
    raise RuntimeError(
        f"No ACS 5-year detail and subject datasets were reachable from {EARLIEST_YEAR} "
        f"through {START_YEAR}."
    )


def to_number(value: str | None) -> float | None:
    if value in {None, "", "-666666666", "-222222222", "-333333333", "-555555555"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def clean_count(value: str | None) -> int | None:
    number = to_number(value)
    return int(number) if number is not None else None


def rate(numerator: int | float | None, denominator: int | float | None) -> float | None:
    if numerator is None or denominator in {None, 0}:
        return None
    return round(float(numerator) / float(denominator), 6)


def state_abbr_from_fips(state_fips: str) -> str:
    return STATE_FIPS_TO_ABBR.get(state_fips, "")


def build_acs_rows(year: int, api_key: str) -> list[dict[str, Any]]:
    detail_rows = fetch_endpoint_data(year, DETAIL_ENDPOINT, api_key)
    subject_rows = fetch_endpoint_data(year, SUBJECT_ENDPOINT, api_key)
    all_county_fips = sorted(set(detail_rows) | set(subject_rows))

    rows: list[dict[str, Any]] = []
    for county_fips in all_county_fips:
        detail = detail_rows.get(county_fips, {})
        subject = subject_rows.get(county_fips, {})
        source = {**detail, **subject}
        state_fips = county_fips[:2]

        raw: dict[str, int | None] = {}
        for field, (_, _, variable_id) in RAW_VARIABLES.items():
            raw[field] = clean_count(source.get(variable_id))

        limited_english_count = sum(
            value or 0
            for value in [
                raw["limited_english_spanish"],
                raw["limited_english_other_indo_european"],
                raw["limited_english_asian_pacific_island"],
                raw["limited_english_other_language"],
            ]
        )
        population_65_plus = sum(
            value or 0
            for field, value in raw.items()
            if field.startswith("male_") or field.startswith("female_")
        )

        row: dict[str, Any] = {
            "county_fips": county_fips,
            "county_name": source.get("NAME", ""),
            "state_fips": state_fips,
            "state_abbr": state_abbr_from_fips(state_fips),
            "acs_year": year,
            "total_population": raw["total_population"],
            "poverty_universe": raw["poverty_universe"],
            "poverty_count": raw["poverty_count"],
            "poverty_rate": rate(raw["poverty_count"], raw["poverty_universe"]),
            "households_total": raw["households_total"],
            "households_no_vehicle": raw["households_no_vehicle"],
            "no_vehicle_rate": rate(raw["households_no_vehicle"], raw["households_total"]),
            "internet_households_total": raw["internet_households_total"],
            "households_without_internet_subscription": raw[
                "households_without_internet_subscription"
            ],
            "no_internet_rate": rate(
                raw["households_without_internet_subscription"],
                raw["internet_households_total"],
            ),
            "limited_english_universe": raw["limited_english_universe"],
            "limited_english_count": limited_english_count,
            "limited_english_rate": rate(
                limited_english_count,
                raw["limited_english_universe"],
            ),
            "population_65_plus": population_65_plus,
            "population_65_plus_rate": rate(
                population_65_plus,
                raw["age_sex_total_population"],
            ),
            "disability_universe": raw["disability_universe"],
            "disability_count": raw["disability_count"],
            "disability_rate": rate(raw["disability_count"], raw["disability_universe"]),
            "race_ethnicity_total": raw["race_ethnicity_total"],
            "non_hispanic_white_count": raw["non_hispanic_white_count"],
            "non_hispanic_white_rate": rate(
                raw["non_hispanic_white_count"],
                raw["race_ethnicity_total"],
            ),
            "non_hispanic_black_count": raw["non_hispanic_black_count"],
            "non_hispanic_black_rate": rate(
                raw["non_hispanic_black_count"],
                raw["race_ethnicity_total"],
            ),
            "hispanic_count": raw["hispanic_count"],
            "hispanic_rate": rate(raw["hispanic_count"], raw["race_ethnicity_total"]),
            "non_hispanic_asian_count": raw["non_hispanic_asian_count"],
            "non_hispanic_asian_rate": rate(
                raw["non_hispanic_asian_count"],
                raw["race_ethnicity_total"],
            ),
            "non_hispanic_aian_count": raw["non_hispanic_aian_count"],
            "non_hispanic_aian_rate": rate(
                raw["non_hispanic_aian_count"],
                raw["race_ethnicity_total"],
            ),
        }
        rows.append(row)
    return rows


def merge_base_with_acs(
    base_rows: list[dict[str, str]],
    acs_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int, int]:
    acs_lookup = {row["county_fips"]: row for row in acs_rows}
    merged_rows = []
    matched = 0
    for base_row in base_rows:
        county_fips = base_row.get("county_fips", "")
        acs_row = acs_lookup.get(county_fips)
        if acs_row:
            matched += 1
            merged_rows.append({**base_row, **acs_row})
        else:
            merged_rows.append(
                {
                    **base_row,
                    **{field: "" for field in ACS_OUTPUT_FIELDS if field not in base_row},
                    "county_fips": county_fips,
                }
            )
    return merged_rows, matched, len(base_rows) - matched


def missingness(rows: list[dict[str, Any]], fields: list[str]) -> dict[str, int]:
    return {
        field: sum(1 for row in rows if row.get(field) in {None, ""}) for field in fields
    }


def rate_ranges(rows: list[dict[str, Any]]) -> dict[str, tuple[float | None, float | None]]:
    ranges = {}
    for field in RATE_FIELDS:
        values = [row[field] for row in rows if row.get(field) not in {None, ""}]
        ranges[field] = (min(values), max(values)) if values else (None, None)
    return ranges


def top_counties(rows: list[dict[str, Any]], field: str, limit: int = 10) -> list[dict[str, Any]]:
    valid_rows = [row for row in rows if row.get(field) not in {None, ""}]
    return sorted(valid_rows, key=lambda row: row[field], reverse=True)[:limit]


def format_missingness(missing: dict[str, int]) -> str:
    return "\n".join(f"- `{field}`: {count}" for field, count in missing.items())


def format_ranges(ranges: dict[str, tuple[float | None, float | None]]) -> str:
    return "\n".join(
        f"- `{field}`: min={min_value}, max={max_value}"
        for field, (min_value, max_value) in ranges.items()
    )


def format_top(rows: list[dict[str, Any]], field: str) -> str:
    return "\n".join(
        f"- {row['county_name']} (`{row['county_fips']}`): {row[field]}"
        for row in rows
    )


def write_summary(
    acs_year: int,
    base_count: int,
    matched_count: int,
    unmatched_count: int,
    acs_rows: list[dict[str, Any]],
) -> None:
    SUMMARY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    run_time = datetime.now().astimezone().isoformat(timespec="seconds")
    missing = missingness(acs_rows, ACS_OUTPUT_FIELDS)
    ranges = rate_ranges(acs_rows)
    indicators = [
        "poverty_rate",
        "no_vehicle_rate",
        "no_internet_rate",
        "limited_english_rate",
        "population_65_plus_rate",
        "disability_rate",
        "race/ethnicity context rates",
    ]
    summary = f"""# ACS Access Indicators Summary

- ACS source: U.S. Census Bureau American Community Survey 5-year API
- ACS vintage/year: {acs_year}
- Input file: `{COUNTY_BASE_INPUT.relative_to(PROJECT_ROOT)}`
- ACS indicator output: `{ACS_OUTPUT.relative_to(PROJECT_ROOT)}`
- Merged output: `{MERGED_OUTPUT.relative_to(PROJECT_ROOT)}`
- Counties in office access base: {base_count}
- Counties with ACS match: {matched_count}
- Counties missing ACS match: {unmatched_count}
- Date/time run: {run_time}

## Indicators Added

{chr(10).join(f"- {indicator}" for indicator in indicators)}

## Missingness By Indicator

{format_missingness(missing)}

## Derived Rate Min/Max Checks

{format_ranges(ranges)}

## Top 10 Counties By Poverty Rate

{format_top(top_counties(acs_rows, "poverty_rate"), "poverty_rate")}

## Top 10 Counties By No-Vehicle Rate

{format_top(top_counties(acs_rows, "no_vehicle_rate"), "no_vehicle_rate")}

## Top 10 Counties By No-Internet Rate

{format_top(top_counties(acs_rows, "no_internet_rate"), "no_internet_rate")}

## Known Limitations

ACS estimates are survey-based and include uncertainty not represented in this first indicator file. County-level indicators may hide important within-county variation. This step adds contextual access-barrier indicators only; it does not calculate a barrier index or add CMS enrollment or rurality data.
"""
    SUMMARY_OUTPUT.write_text(summary, encoding="utf-8")


def main() -> int:
    base_rows = read_csv_rows(COUNTY_BASE_INPUT)
    api_key = get_api_key()
    acs_year = discover_acs_year(api_key)
    acs_rows = build_acs_rows(acs_year, api_key)

    write_csv_rows(ACS_OUTPUT, acs_rows, ACS_OUTPUT_FIELDS)

    merged_rows, matched_count, unmatched_count = merge_base_with_acs(base_rows, acs_rows)
    merged_fieldnames = list(dict.fromkeys([*base_rows[0].keys(), *ACS_OUTPUT_FIELDS]))
    write_csv_rows(MERGED_OUTPUT, merged_rows, merged_fieldnames)

    write_summary(
        acs_year=acs_year,
        base_count=len(base_rows),
        matched_count=matched_count,
        unmatched_count=unmatched_count,
        acs_rows=acs_rows,
    )

    print(f"ACS year/vintage used: {acs_year}")
    print(f"Number of counties in office access base: {len(base_rows)}")
    print(f"Number of counties with ACS match: {matched_count}")
    print(f"Number of counties missing ACS match: {unmatched_count}")
    print("Missingness by indicator:")
    for field, count in missingness(acs_rows, ACS_OUTPUT_FIELDS).items():
        print(f"- {field}: {count}")
    print("Basic min/max checks for derived rates:")
    for field, (min_value, max_value) in rate_ranges(acs_rows).items():
        print(f"- {field}: min={min_value}, max={max_value}")
    print("Top 10 counties by poverty_rate:")
    for row in top_counties(acs_rows, "poverty_rate"):
        print(f"- {row['county_name']} ({row['county_fips']}): {row['poverty_rate']}")
    print("Top 10 counties by no_vehicle_rate:")
    for row in top_counties(acs_rows, "no_vehicle_rate"):
        print(f"- {row['county_name']} ({row['county_fips']}): {row['no_vehicle_rate']}")
    print("Top 10 counties by no_internet_rate:")
    for row in top_counties(acs_rows, "no_internet_rate"):
        print(f"- {row['county_name']} ({row['county_fips']}): {row['no_internet_rate']}")
    print(f"Wrote ACS indicators: {ACS_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote merged county file: {MERGED_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote summary: {SUMMARY_OUTPUT.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
