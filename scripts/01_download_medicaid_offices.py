"""Download helper for the Shafer et al. Medicaid office locations dataset.

Expected raw file path:
    data/raw/medicaid_offices.xlsx

The Harvard Dataverse dataset is identified by DOI 10.7910/DVN/AVRHMI. This
script uses the Dataverse API to inspect available files and downloads an Excel
file only if one can be identified unambiguously. It does not use fake URLs or
create placeholder data.
"""

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "medicaid_offices.xlsx"
DATASET_PID = "doi:10.7910/DVN/AVRHMI"
DATAVERSE_API_BASE = "https://dataverse.harvard.edu/api"
INSTRUCTIONS_PATH = PROJECT_ROOT / "docs" / "data_download_instructions.md"


def fail_with_manual_instructions(message: str) -> int:
    print(message)
    print(f"Manual download instructions: {INSTRUCTIONS_PATH.relative_to(PROJECT_ROOT)}")
    return 1


def fetch_json(url: str) -> dict:
    with urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download_file(file_id: int, destination: Path) -> None:
    url = f"{DATAVERSE_API_BASE}/access/datafile/{file_id}"
    with urlopen(url, timeout=60) as response:
        destination.write_bytes(response.read())


def find_excel_file_id(dataset_metadata: dict) -> int | None:
    files = dataset_metadata.get("data", {}).get("latestVersion", {}).get("files", [])
    excel_files = []

    for file_info in files:
        data_file = file_info.get("dataFile", {})
        filename = data_file.get("filename", "")
        content_type = data_file.get("contentType", "")
        file_id = data_file.get("id")

        if file_id and (
            filename.lower().endswith((".xlsx", ".xls"))
            or "spreadsheet" in content_type.lower()
            or "excel" in content_type.lower()
        ):
            excel_files.append(file_id)

    if len(excel_files) == 1:
        return excel_files[0]

    return None


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if OUTPUT_FILE.exists():
        print(f"FOUND existing raw file: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
        return 0

    query = urlencode({"persistentId": DATASET_PID})
    metadata_url = f"{DATAVERSE_API_BASE}/datasets/:persistentId/?{query}"

    try:
        dataset_metadata = fetch_json(metadata_url)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return fail_with_manual_instructions(
            "Automated Dataverse lookup failed. "
            f"Download the file manually instead. Details: {exc}"
        )

    file_id = find_excel_file_id(dataset_metadata)
    if file_id is None:
        return fail_with_manual_instructions(
            "Could not identify a single Excel file from the Dataverse metadata."
        )

    try:
        download_file(file_id, OUTPUT_FILE)
    except (HTTPError, URLError, TimeoutError) as exc:
        if OUTPUT_FILE.exists():
            OUTPUT_FILE.unlink()
        return fail_with_manual_instructions(
            "Automated Dataverse download failed. "
            f"Download the file manually instead. Details: {exc}"
        )

    print(f"Downloaded raw Medicaid office file to: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
