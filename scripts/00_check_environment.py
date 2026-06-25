"""Check the local project structure and expected raw data file."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIRECTORIES = [
    PROJECT_ROOT / "data" / "raw",
    PROJECT_ROOT / "data" / "processed",
    PROJECT_ROOT / "data" / "manual",
    PROJECT_ROOT / "scripts",
    PROJECT_ROOT / "powerbi",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "outputs",
]
RAW_MEDICAID_OFFICES = PROJECT_ROOT / "data" / "raw" / "medicaid_offices.xlsx"


def main() -> int:
    print("Checking Medicaid Access Barriers project environment...")

    missing_dirs = [path for path in EXPECTED_DIRECTORIES if not path.is_dir()]
    if missing_dirs:
        print("MISSING expected folders:")
        for path in missing_dirs:
            print(f"- {path.relative_to(PROJECT_ROOT)}")
    else:
        print("FOUND expected folder structure.")

    if RAW_MEDICAID_OFFICES.exists():
        print(f"FOUND raw Medicaid office file: {RAW_MEDICAID_OFFICES.relative_to(PROJECT_ROOT)}")
    else:
        print(
            "MISSING raw Medicaid office file: "
            f"{RAW_MEDICAID_OFFICES.relative_to(PROJECT_ROOT)}"
        )
        print("Download instructions: docs/data_download_instructions.md")

    return 1 if missing_dirs else 0


if __name__ == "__main__":
    raise SystemExit(main())
