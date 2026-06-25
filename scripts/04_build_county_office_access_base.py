"""Build the complete county office access base table.

Inputs:
    data/processed/medicaid_offices_with_county.csv

Outputs:
    data/processed/county_office_access_base.csv
    data/processed/state_office_access_base.csv
    outputs/county_office_access_base_summary.md

This step creates a complete county/county-equivalent table for the 50 states
and D.C., joins Medicaid office counts, and flags zero-office counties. It does
not add ACS indicators, CMS enrollment, rurality, Power BI files, or barrier
index calculations.
"""

from __future__ import annotations

import csv
import importlib.util
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OFFICE_COUNTY_INPUT = PROJECT_ROOT / "data" / "processed" / "medicaid_offices_with_county.csv"
COUNTY_BASE_OUTPUT = PROJECT_ROOT / "data" / "processed" / "county_office_access_base.csv"
STATE_BASE_OUTPUT = PROJECT_ROOT / "data" / "processed" / "state_office_access_base.csv"
SUMMARY_OUTPUT = PROJECT_ROOT / "outputs" / "county_office_access_base_summary.md"
COUNTY_ASSIGNMENT_SCRIPT = PROJECT_ROOT / "scripts" / "03_assign_offices_to_counties.py"

# Analytic universe: the Medicaid office dataset covers the 50 states and
# District of Columbia. Territories are intentionally excluded here and in the
# ACS indicator step so all downstream county files use the same geography.
ANALYTIC_STATE_FIPS_50_DC = {
    "01",
    "02",
    "04",
    "05",
    "06",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "53",
    "54",
    "55",
    "56",
}

COUNTY_BASE_FIELDS = [
    "county_fips",
    "county_name",
    "state_abbr",
    "state_fips",
    "state_name",
    "office_count",
    "has_medicaid_office",
]

STATE_BASE_FIELDS = [
    "state_fips",
    "state_abbr",
    "state_name",
    "office_count",
    "total_counties",
    "counties_with_office",
    "counties_without_office",
    "share_counties_with_office",
    "share_counties_without_office",
]


def load_county_assignment_module() -> Any:
    spec = importlib.util.spec_from_file_location("county_assignment", COUNTY_ASSIGNMENT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load scripts/03_assign_offices_to_counties.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing expected input: {path.relative_to(PROJECT_ROOT)}. "
            "Run scripts/03_assign_offices_to_counties.py first."
        )
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_county_base(
    counties: list[dict[str, Any]],
    office_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    office_counts = Counter(row["county_fips"] for row in office_rows if row.get("county_fips"))
    county_rows = []

    for county in sorted(counties, key=lambda item: item["county_fips"]):
        office_count = office_counts.get(county["county_fips"], 0)
        county_rows.append(
            {
                "county_fips": county["county_fips"],
                "county_name": county["county_name"],
                "state_abbr": county["state_abbr"],
                "state_fips": county["state_fips"],
                "state_name": county["state_name"],
                "office_count": office_count,
                "has_medicaid_office": 1 if office_count > 0 else 0,
            }
        )

    return county_rows


def build_state_base(county_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in county_rows:
        grouped[row["state_fips"]].append(row)

    state_rows = []
    for state_fips, rows in sorted(grouped.items()):
        total_counties = len(rows)
        office_count = sum(int(row["office_count"]) for row in rows)
        counties_with_office = sum(1 for row in rows if int(row["office_count"]) > 0)
        counties_without_office = total_counties - counties_with_office
        state_rows.append(
            {
                "state_fips": state_fips,
                "state_abbr": rows[0]["state_abbr"],
                "state_name": rows[0]["state_name"],
                "office_count": office_count,
                "total_counties": total_counties,
                "counties_with_office": counties_with_office,
                "counties_without_office": counties_without_office,
                "share_counties_with_office": round(counties_with_office / total_counties, 6)
                if total_counties
                else "",
                "share_counties_without_office": round(
                    counties_without_office / total_counties,
                    6,
                )
                if total_counties
                else "",
            }
        )

    return state_rows


def format_top_states_by_count(state_rows: list[dict[str, Any]]) -> str:
    rows = sorted(state_rows, key=lambda row: row["office_count"], reverse=True)[:10]
    return "\n".join(
        f"- {row['state_abbr']}: {row['office_count']} offices" for row in rows
    )


def format_top_states_by_zero_share(state_rows: list[dict[str, Any]]) -> str:
    rows = sorted(
        state_rows,
        key=lambda row: row["share_counties_without_office"],
        reverse=True,
    )[:10]
    return "\n".join(
        "- "
        f"{row['state_abbr']}: {row['share_counties_without_office']} "
        f"({row['counties_without_office']} of {row['total_counties']} counties)"
        for row in rows
    )


def write_summary(
    county_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    boundary_source_name: str,
    boundary_layer: str,
    boundary_url: str,
) -> None:
    SUMMARY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    run_time = datetime.now().astimezone().isoformat(timespec="seconds")
    total_counties = len(county_rows)
    total_offices = sum(int(row["office_count"]) for row in county_rows)
    counties_with_office = sum(1 for row in county_rows if int(row["office_count"]) > 0)
    counties_without_office = total_counties - counties_with_office
    summary = f"""# County Office Access Base Summary

- Boundary/reference source: {boundary_source_name}, {boundary_layer}
- Boundary file URL: `{boundary_url}`
- Analytic universe: 50 states and District of Columbia
- Territories excluded: Yes, because the Medicaid office dataset covers the 50 states and D.C.
- Office input file: `{OFFICE_COUNTY_INPUT.relative_to(PROJECT_ROOT)}`
- County base output: `{COUNTY_BASE_OUTPUT.relative_to(PROJECT_ROOT)}`
- State base output: `{STATE_BASE_OUTPUT.relative_to(PROJECT_ROOT)}`
- Total counties/county equivalents: {total_counties}
- Total offices counted: {total_offices}
- Counties with office: {counties_with_office}
- Counties without office: {counties_without_office}
- States/DC represented: {len(state_rows)}
- Date/time run: {run_time}

## Top 10 States By Office Count

{format_top_states_by_count(state_rows)}

## Top 10 States By Share Of Counties Without An Office

{format_top_states_by_zero_share(state_rows)}

## Notes

This table uses the same Census cartographic county boundary source as the county assignment step and includes counties with zero Medicaid offices. It covers the 50 states and D.C. only, matching the geography of the Medicaid office dataset. Puerto Rico and other territories are excluded from the analytic universe. State-level office counts are based on assigned county geography, not the original source `state` field.
"""
    SUMMARY_OUTPUT.write_text(summary, encoding="utf-8")


def main() -> int:
    county_assignment = load_county_assignment_module()
    office_rows = read_csv_rows(OFFICE_COUNTY_INPUT)

    counties = county_assignment.load_counties_from_boundary_zip(ANALYTIC_STATE_FIPS_50_DC)
    county_rows = build_county_base(counties, office_rows)
    state_rows = build_state_base(county_rows)

    write_csv_rows(COUNTY_BASE_OUTPUT, county_rows, COUNTY_BASE_FIELDS)
    write_csv_rows(STATE_BASE_OUTPUT, state_rows, STATE_BASE_FIELDS)
    write_summary(
        county_rows=county_rows,
        state_rows=state_rows,
        boundary_source_name=county_assignment.BOUNDARY_SOURCE_NAME,
        boundary_layer=county_assignment.BOUNDARY_LAYER,
        boundary_url=county_assignment.BOUNDARY_URL,
    )

    total_offices = sum(int(row["office_count"]) for row in county_rows)
    counties_with_office = sum(1 for row in county_rows if int(row["office_count"]) > 0)
    counties_without_office = len(county_rows) - counties_with_office

    print(f"Total counties/county equivalents: {len(county_rows)}")
    print(f"Total offices counted: {total_offices}")
    print(f"Counties with office: {counties_with_office}")
    print(f"Counties without office: {counties_without_office}")
    print(f"States/DC represented: {len(state_rows)}")
    print("Top 10 states by office count:")
    print(format_top_states_by_count(state_rows))
    print("Top 10 states by share of counties without an office:")
    print(format_top_states_by_zero_share(state_rows))
    print(f"Wrote county base: {COUNTY_BASE_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote state base: {STATE_BASE_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote summary: {SUMMARY_OUTPUT.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
