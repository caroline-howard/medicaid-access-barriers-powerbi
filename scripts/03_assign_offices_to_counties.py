"""Assign cleaned Medicaid office locations to U.S. counties.

Input:
    data/processed/medicaid_offices_clean.csv

Outputs:
    data/processed/medicaid_offices_with_county.csv
    data/processed/county_office_counts.csv
    data/processed/state_office_summary.csv
    outputs/county_assignment_summary.md
    outputs/offices_without_county_match.csv, only when unmatched offices exist

This step only assigns offices to counties and creates office-count summaries.
It does not add ACS indicators, CMS enrollment data, rurality fields, Power BI
files, or barrier index calculations.
"""

from __future__ import annotations

import csv
import math
import struct
import zipfile
from collections import Counter, defaultdict
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "medicaid_offices_clean.csv"
MANUAL_ASSIGNMENTS_FILE = PROJECT_ROOT / "data" / "manual" / "manual_county_assignments.csv"
OFFICE_COUNTY_OUTPUT = PROJECT_ROOT / "data" / "processed" / "medicaid_offices_with_county.csv"
COUNTY_COUNTS_OUTPUT = PROJECT_ROOT / "data" / "processed" / "county_office_counts.csv"
STATE_SUMMARY_OUTPUT = PROJECT_ROOT / "data" / "processed" / "state_office_summary.csv"
SUMMARY_OUTPUT = PROJECT_ROOT / "outputs" / "county_assignment_summary.md"
UNMATCHED_OUTPUT = PROJECT_ROOT / "outputs" / "offices_without_county_match.csv"

BOUNDARY_SOURCE_NAME = "U.S. Census cartographic boundary county shapefile"
BOUNDARY_LAYER = "cb_2025_us_county_500k"
BOUNDARY_URL = "https://www2.census.gov/geo/tiger/GENZ2025/shp/cb_2025_us_county_500k.zip"
NEAREST_COUNTY_FALLBACK_THRESHOLD_MILES = 5.0
KM_PER_MILE = 1.609344
EARTH_RADIUS_MILES = 3958.7613

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

STATE_ABBR_TO_NAME = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "AS": "American Samoa",
    "GU": "Guam",
    "MP": "Northern Mariana Islands",
    "PR": "Puerto Rico",
    "VI": "U.S. Virgin Islands",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing input file: {path.relative_to(PROJECT_ROOT)}. "
            "Run scripts/02_clean_medicaid_offices.py first."
        )
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def read_manual_assignments(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        return {
            row["office_id"]: row
            for row in csv.DictReader(csv_file)
            if row.get("office_id")
        }


def ring_bbox(ring: list[list[float]]) -> tuple[float, float, float, float]:
    xs = [point[0] for point in ring]
    ys = [point[1] for point in ring]
    return min(xs), min(ys), max(xs), max(ys)


def bbox_contains(bbox: tuple[float, float, float, float], lon: float, lat: float) -> bool:
    min_lon, min_lat, max_lon, max_lat = bbox
    return min_lon <= lon <= max_lon and min_lat <= lat <= max_lat


def point_in_ring(lon: float, lat: float, ring: list[list[float]]) -> bool:
    inside = False
    if len(ring) < 3:
        return inside

    previous_lon, previous_lat = ring[-1]
    for current_lon, current_lat in ring:
        crosses_lat = (current_lat > lat) != (previous_lat > lat)
        if crosses_lat:
            slope_lon = (
                (previous_lon - current_lon)
                * (lat - current_lat)
                / (previous_lat - current_lat)
                + current_lon
            )
            if lon < slope_lon:
                inside = not inside
        previous_lon, previous_lat = current_lon, current_lat

    return inside


def point_in_polygon(lon: float, lat: float, polygon: list[list[list[float]]]) -> bool:
    inside = False
    for ring in polygon:
        if point_in_ring(lon, lat, ring):
            inside = not inside
    return inside


def haversine_miles(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_MILES * math.asin(math.sqrt(a))


def point_to_segment_distance_miles(
    lon: float,
    lat: float,
    start: list[float],
    end: list[float],
) -> float:
    start_lon, start_lat = start
    end_lon, end_lat = end
    mean_lat_rad = math.radians((lat + start_lat + end_lat) / 3)

    point_x = lon * math.cos(mean_lat_rad)
    point_y = lat
    start_x = start_lon * math.cos(mean_lat_rad)
    start_y = start_lat
    end_x = end_lon * math.cos(mean_lat_rad)
    end_y = end_lat

    dx = end_x - start_x
    dy = end_y - start_y
    if dx == 0 and dy == 0:
        return haversine_miles(lon, lat, start_lon, start_lat)

    t = ((point_x - start_x) * dx + (point_y - start_y) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    nearest_x = start_x + t * dx
    nearest_y = start_y + t * dy
    nearest_lon = nearest_x / math.cos(mean_lat_rad) if math.cos(mean_lat_rad) else start_lon
    nearest_lat = nearest_y
    return haversine_miles(lon, lat, nearest_lon, nearest_lat)


def point_to_ring_distance_miles(lon: float, lat: float, ring: list[list[float]]) -> float:
    if not ring:
        return float("inf")
    distances = []
    for index, start in enumerate(ring):
        end = ring[(index + 1) % len(ring)]
        distances.append(point_to_segment_distance_miles(lon, lat, start, end))
    return min(distances)


def point_to_polygon_distance_miles(
    lon: float,
    lat: float,
    polygon: list[list[list[float]]],
) -> float:
    if point_in_polygon(lon, lat, polygon):
        return 0.0
    return min(point_to_ring_distance_miles(lon, lat, ring) for ring in polygon if ring)


def download_boundary_zip() -> bytes:
    try:
        with urlopen(BOUNDARY_URL, timeout=90) as response:
            return response.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Could not download Census county boundary ZIP: {exc}") from exc


def read_dbf_records(dbf_bytes: bytes) -> list[dict[str, str]]:
    record_count = struct.unpack("<I", dbf_bytes[4:8])[0]
    header_length = struct.unpack("<H", dbf_bytes[8:10])[0]
    record_length = struct.unpack("<H", dbf_bytes[10:12])[0]

    fields = []
    offset = 32
    while dbf_bytes[offset] != 0x0D:
        descriptor = dbf_bytes[offset : offset + 32]
        name = descriptor[:11].split(b"\x00", 1)[0].decode("ascii").strip()
        length = descriptor[16]
        fields.append((name, length))
        offset += 32

    records = []
    for index in range(record_count):
        start = header_length + index * record_length
        record = dbf_bytes[start : start + record_length]
        if not record or record[:1] == b"*":
            continue

        position = 1
        parsed_record: dict[str, str] = {}
        for name, length in fields:
            raw_value = record[position : position + length]
            parsed_record[name] = raw_value.decode("latin1").strip()
            position += length
        records.append(parsed_record)

    return records


def read_shp_polygons(shp_bytes: bytes) -> list[dict[str, Any]]:
    position = 100
    shapes = []
    while position < len(shp_bytes):
        if position + 8 > len(shp_bytes):
            break
        content_length_words = struct.unpack(">i", shp_bytes[position + 4 : position + 8])[0]
        content_length = content_length_words * 2
        content_start = position + 8
        content = shp_bytes[content_start : content_start + content_length]
        position = content_start + content_length

        if len(content) < 44:
            continue
        shape_type = struct.unpack("<i", content[:4])[0]
        if shape_type not in {5, 15}:  # Polygon or PolygonZ
            shapes.append({"rings": [], "bbox": (0, 0, 0, 0)})
            continue

        min_lon, min_lat, max_lon, max_lat = struct.unpack("<4d", content[4:36])
        num_parts, num_points = struct.unpack("<2i", content[36:44])
        parts_start = 44
        points_start = parts_start + num_parts * 4
        parts = list(struct.unpack(f"<{num_parts}i", content[parts_start:points_start]))

        points = []
        for point_index in range(num_points):
            point_start = points_start + point_index * 16
            lon, lat = struct.unpack("<2d", content[point_start : point_start + 16])
            points.append([lon, lat])

        rings = []
        for part_index, start_index in enumerate(parts):
            end_index = parts[part_index + 1] if part_index + 1 < len(parts) else num_points
            rings.append(points[start_index:end_index])

        shapes.append({"rings": rings, "bbox": (min_lon, min_lat, max_lon, max_lat)})

    return shapes


def load_counties_from_boundary_zip(state_fips_values: set[str]) -> list[dict[str, Any]]:
    boundary_bytes = download_boundary_zip()
    with zipfile.ZipFile(BytesIO(boundary_bytes)) as archive:
        shp_name = next(name for name in archive.namelist() if name.endswith(".shp"))
        dbf_name = next(name for name in archive.namelist() if name.endswith(".dbf"))
        shapes = read_shp_polygons(archive.read(shp_name))
        records = read_dbf_records(archive.read(dbf_name))

    if len(shapes) != len(records):
        raise RuntimeError(
            f"Boundary shape/record count mismatch: {len(shapes)} shapes, {len(records)} records"
        )

    counties: list[dict[str, Any]] = []
    for record, shape in zip(records, shapes, strict=True):
        state_fips = str(record.get("STATEFP", "")).zfill(2)
        if state_fips not in state_fips_values:
            continue
        state_abbr = STATE_FIPS_TO_ABBR.get(state_fips, "")
        county_fips = str(record.get("GEOID", ""))
        county_name = str(record.get("NAMELSAD") or record.get("NAME", ""))
        if shape["rings"]:
            counties.append(
                {
                    "county_fips": county_fips,
                    "county_name": county_name,
                    "state_fips": state_fips,
                    "state_abbr": state_abbr,
                    "state_name": STATE_ABBR_TO_NAME.get(state_abbr, ""),
                    "polygons": [shape],
                }
            )
    return counties


def assign_county(
    lon: float,
    lat: float,
    counties_by_state: dict[str, list[dict[str, Any]]],
    state_abbr: str,
) -> dict[str, Any] | None:
    candidate_counties = counties_by_state.get(state_abbr, [])
    for county in candidate_counties:
        for polygon in county["polygons"]:
            if bbox_contains(polygon["bbox"], lon, lat) and point_in_polygon(
                lon, lat, polygon["rings"]
            ):
                return county

    # Fallback in case source state abbreviations differ from boundary state abbreviations.
    for counties in counties_by_state.values():
        for county in counties:
            for polygon in county["polygons"]:
                if bbox_contains(polygon["bbox"], lon, lat) and point_in_polygon(
                    lon, lat, polygon["rings"]
                ):
                    return county
    return None


def nearest_county_candidate(
    lon: float,
    lat: float,
    counties_by_state: dict[str, list[dict[str, Any]]],
    state_abbr: str,
) -> tuple[dict[str, Any], float] | None:
    nearest_county = None
    nearest_distance = float("inf")
    for county in counties_by_state.get(state_abbr, []):
        for polygon in county["polygons"]:
            distance = point_to_polygon_distance_miles(lon, lat, polygon["rings"])
            if distance < nearest_distance:
                nearest_county = county
                nearest_distance = distance

    if nearest_county is not None:
        return nearest_county, nearest_distance
    return None


def nearest_county_fallback(
    lon: float,
    lat: float,
    counties_by_state: dict[str, list[dict[str, Any]]],
    state_abbr: str,
) -> tuple[dict[str, Any], float] | None:
    candidate = nearest_county_candidate(lon, lat, counties_by_state, state_abbr)
    if candidate is None:
        return None
    nearest_county, nearest_distance = candidate
    if (
        nearest_distance <= NEAREST_COUNTY_FALLBACK_THRESHOLD_MILES
    ):
        return nearest_county, nearest_distance
    return None


def write_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_county_counts(assigned_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    counts = Counter(row["county_fips"] for row in assigned_rows if row.get("county_fips"))
    county_lookup = {
        row["county_fips"]: {
            "county_fips": row["county_fips"],
            "county_name": row["county_name"],
            "state_abbr": row["county_state_abbr"],
            "state_name": STATE_ABBR_TO_NAME.get(row["county_state_abbr"], ""),
        }
        for row in assigned_rows
        if row.get("county_fips")
    }
    output = []
    for county_fips, count in sorted(counts.items()):
        row = dict(county_lookup[county_fips])
        row["office_count"] = count
        output.append(row)
    return output


def build_state_summary(
    assigned_rows: list[dict[str, str]],
    counties: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    office_counts = Counter(row.get("state", "") for row in assigned_rows)
    counties_with_office: dict[str, set[str]] = defaultdict(set)
    total_counties = Counter(county["state_abbr"] for county in counties if county["state_abbr"])

    for row in assigned_rows:
        state_abbr = row.get("state", "")
        county_fips = row.get("county_fips", "")
        if state_abbr and county_fips:
            counties_with_office[state_abbr].add(county_fips)

    output = []
    for state_abbr, office_count in sorted(office_counts.items()):
        total = total_counties.get(state_abbr, 0)
        county_count = len(counties_with_office.get(state_abbr, set()))
        output.append(
            {
                "state_fips": next(
                    (fips for fips, abbr in STATE_FIPS_TO_ABBR.items() if abbr == state_abbr),
                    "",
                ),
                "state_name": STATE_ABBR_TO_NAME.get(state_abbr, ""),
                "state_abbr": state_abbr,
                "office_count": office_count,
                "county_count_with_office": county_count,
                "total_counties": total,
                "share_counties_with_office": round(county_count / total, 4) if total else "",
            }
        )
    return output


def write_summary(
    offices_read: int,
    direct_spatial_matches: int,
    fallback_matches: int,
    manual_matches: int,
    unmatched_rows: list[dict[str, str]],
    county_count: int,
    state_count: int,
    top_states: list[tuple[str, int]],
) -> None:
    SUMMARY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    run_time = datetime.now().astimezone().isoformat(timespec="seconds")
    unmatched_note = (
        f"Unmatched offices were written to `{UNMATCHED_OUTPUT.relative_to(PROJECT_ROOT)}` "
        "with nearest-county distance fields for review."
        if unmatched_rows
        else (
            "No unmatched offices were found; "
            f"`{UNMATCHED_OUTPUT.relative_to(PROJECT_ROOT)}` contains headers only."
        )
    )
    top_states_text = "\n".join(f"- {state}: {count}" for state, count in top_states)
    summary = f"""# County Assignment Summary

- Input file: `{INPUT_FILE.relative_to(PROJECT_ROOT)}`
- Office-level output: `{OFFICE_COUNTY_OUTPUT.relative_to(PROJECT_ROOT)}`
- County count output: `{COUNTY_COUNTS_OUTPUT.relative_to(PROJECT_ROOT)}`
- State summary output: `{STATE_SUMMARY_OUTPUT.relative_to(PROJECT_ROOT)}`
- Manual assignment crosswalk: `{MANUAL_ASSIGNMENTS_FILE.relative_to(PROJECT_ROOT)}`
- Boundary source used: {BOUNDARY_SOURCE_NAME}, {BOUNDARY_LAYER}
- Boundary file URL: `{BOUNDARY_URL}`
- Offices read: {offices_read}
- Offices matched by direct spatial join: {direct_spatial_matches}
- Offices matched by nearest-county fallback: {fallback_matches}
- Offices matched by manual review crosswalk: {manual_matches}
- Offices unmatched: {len(unmatched_rows)}
- Fallback distance threshold: {NEAREST_COUNTY_FALLBACK_THRESHOLD_MILES} miles ({round(NEAREST_COUNTY_FALLBACK_THRESHOLD_MILES * KM_PER_MILE, 2)} km)
- Counties with at least one office: {county_count}
- States/DC represented: {state_count}
- Date/time run: {run_time}

## Top 10 States By Office Count

{top_states_text}

## Unmatched Offices

{unmatched_note}

## Manual Review Crosswalk

Manual county assignments are applied only after direct spatial join and nearest-county fallback fail. The crosswalk is limited to reviewed records in `{MANUAL_ASSIGNMENTS_FILE.relative_to(PROJECT_ROOT)}` and uses `county_match_method = manual_review_crosswalk`.

## Limitations

County assignment first uses office latitude/longitude points and Census 2025 cartographic county boundaries for a direct point-in-polygon spatial join. For offices that do not fall inside a generalized county polygon, the script applies a conservative nearest-county fallback using the same boundary file only when the nearest county boundary is within {NEAREST_COUNTY_FALLBACK_THRESHOLD_MILES} miles. Reviewed manual assignments are applied after those automated steps only. This is appropriate for county-level summaries but does not measure travel distance, within-county access variation, or whether an office serves residents across county or state lines. Boundary vintages may differ from the late-2023 office dataset. Any offices still unmatched after fallback and manual review are exported for review instead of being forced into a county.
"""
    SUMMARY_OUTPUT.write_text(summary, encoding="utf-8")


def main() -> int:
    office_rows = read_csv(INPUT_FILE)
    manual_assignments = read_manual_assignments(MANUAL_ASSIGNMENTS_FILE)
    state_fips_values = sorted(
        {
            str(row.get("state_fips", "")).zfill(2)
            for row in office_rows
            if row.get("state_fips", "")
        }
    )
    print("Downloading Census county cartographic boundary shapefile...", flush=True)
    counties = load_counties_from_boundary_zip(set(state_fips_values))
    print(f"Loaded {len(counties)} county boundary features.", flush=True)
    counties_by_state: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for county in counties:
        counties_by_state[county["state_abbr"]].append(county)

    assigned_rows: list[dict[str, str]] = []
    unmatched_rows: list[dict[str, str]] = []
    direct_spatial_matches = 0
    fallback_matches = 0
    manual_matches = 0

    for row in office_rows:
        output_row = dict(row)
        try:
            lat = float(row.get("latitude", ""))
            lon = float(row.get("longitude", ""))
        except ValueError:
            output_row.update(
                {
                    "county_fips": "",
                    "county_name": "",
                    "county_state_abbr": "",
                    "county_match_method": "unmatched",
                    "county_match_distance_miles": "",
                    "county_match_distance_km": "",
                }
            )
            unmatched_rows.append(output_row)
            continue

        county = assign_county(lon, lat, counties_by_state, row.get("state", ""))
        if county:
            output_row.update(
                {
                    "county_fips": county["county_fips"],
                    "county_name": county["county_name"],
                    "county_state_abbr": county["state_abbr"],
                    "county_match_method": "spatial_join",
                    "county_match_distance_miles": "0",
                    "county_match_distance_km": "0",
                }
            )
            assigned_rows.append(output_row)
            direct_spatial_matches += 1
        else:
            fallback_candidate = nearest_county_candidate(
                lon, lat, counties_by_state, row.get("state", "")
            )
            fallback = (
                fallback_candidate
                if fallback_candidate
                and fallback_candidate[1] <= NEAREST_COUNTY_FALLBACK_THRESHOLD_MILES
                else None
            )
            if fallback:
                fallback_county, distance_miles = fallback
                output_row.update(
                    {
                        "county_fips": fallback_county["county_fips"],
                        "county_name": fallback_county["county_name"],
                        "county_state_abbr": fallback_county["state_abbr"],
                        "county_match_method": "nearest_county_fallback",
                        "county_match_distance_miles": round(distance_miles, 4),
                        "county_match_distance_km": round(distance_miles * KM_PER_MILE, 4),
                    }
                )
                assigned_rows.append(output_row)
                fallback_matches += 1
            else:
                nearest_distance_miles = fallback_candidate[1] if fallback_candidate else ""
                nearest_distance_km = (
                    fallback_candidate[1] * KM_PER_MILE if fallback_candidate else ""
                )
                manual_assignment = manual_assignments.get(row.get("office_id", ""))
                if manual_assignment:
                    output_row.update(
                        {
                            "county_fips": manual_assignment["county_fips"],
                            "county_name": manual_assignment["county_name"],
                            "county_state_abbr": manual_assignment["county_state_abbr"],
                            "county_match_method": "manual_review_crosswalk",
                            "county_match_distance_miles": (
                                round(nearest_distance_miles, 4)
                                if nearest_distance_miles != ""
                                else ""
                            ),
                            "county_match_distance_km": (
                                round(nearest_distance_km, 4)
                                if nearest_distance_km != ""
                                else ""
                            ),
                        }
                    )
                    assigned_rows.append(output_row)
                    manual_matches += 1
                else:
                    output_row.update(
                        {
                            "county_fips": "",
                            "county_name": "",
                            "county_state_abbr": "",
                            "county_match_method": "unmatched",
                            "county_match_distance_miles": (
                                round(nearest_distance_miles, 4)
                                if nearest_distance_miles != ""
                                else ""
                            ),
                            "county_match_distance_km": (
                                round(nearest_distance_km, 4)
                                if nearest_distance_km != ""
                                else ""
                            ),
                        }
                    )
                    unmatched_rows.append(output_row)

    office_fieldnames = list(office_rows[0].keys()) + [
        "county_fips",
        "county_name",
        "county_state_abbr",
        "county_match_method",
        "county_match_distance_miles",
        "county_match_distance_km",
    ]
    write_rows(OFFICE_COUNTY_OUTPUT, assigned_rows + unmatched_rows, office_fieldnames)

    county_counts = build_county_counts(assigned_rows)
    write_rows(
        COUNTY_COUNTS_OUTPUT,
        county_counts,
        ["county_fips", "county_name", "state_abbr", "state_name", "office_count"],
    )

    state_summary = build_state_summary(assigned_rows, counties)
    write_rows(
        STATE_SUMMARY_OUTPUT,
        state_summary,
        [
            "state_fips",
            "state_name",
            "state_abbr",
            "office_count",
            "county_count_with_office",
            "total_counties",
            "share_counties_with_office",
        ],
    )

    write_rows(UNMATCHED_OUTPUT, unmatched_rows, office_fieldnames)

    state_counts = Counter(row.get("state", "") for row in assigned_rows)
    top_states = state_counts.most_common(10)
    write_summary(
        offices_read=len(office_rows),
        direct_spatial_matches=direct_spatial_matches,
        fallback_matches=fallback_matches,
        manual_matches=manual_matches,
        unmatched_rows=unmatched_rows,
        county_count=len(county_counts),
        state_count=len(state_counts),
        top_states=top_states,
    )

    print(f"Number of offices read: {len(office_rows)}")
    print(f"Number of offices assigned to counties: {len(assigned_rows)}")
    print(f"Number matched by direct spatial join: {direct_spatial_matches}")
    print(f"Number matched by nearest-county fallback: {fallback_matches}")
    print(f"Number matched by manual review crosswalk: {manual_matches}")
    print(
        "Nearest-county fallback threshold: "
        f"{NEAREST_COUNTY_FALLBACK_THRESHOLD_MILES} miles"
    )
    print(f"Number of offices not assigned to counties: {len(unmatched_rows)}")
    print(f"Number of counties with at least one office: {len(county_counts)}")
    print(f"Number of states/DC represented: {len(state_counts)}")
    print("Top 10 states by office count:")
    for state, count in top_states:
        print(f"- {state}: {count}")
    if unmatched_rows:
        print(f"Unmatched offices written to: {UNMATCHED_OUTPUT.relative_to(PROJECT_ROOT)}")
    else:
        print("Any unmatched offices: none")
    print(f"Wrote office county assignment: {OFFICE_COUNTY_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote county office counts: {COUNTY_COUNTS_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote state office summary: {STATE_SUMMARY_OUTPUT.relative_to(PROJECT_ROOT)}")
    print(f"Wrote county assignment summary: {SUMMARY_OUTPUT.relative_to(PROJECT_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
