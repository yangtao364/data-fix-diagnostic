"""Small regression checks for the public fixtures.

Run from the repository root with: python tests/test_diagnostic.py
"""
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "diagnose_csv.py"


def report(relative_path: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(ROOT / relative_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_trimmed_full_row_duplicate():
    got = report("sample/case-duplicate-whitespace.csv")
    assert got["rows"] == 3
    assert got["duplicate_rows"] == 1
    assert got["blank_counts"] == {"record_id": 0, "email": 0, "amount": 0}
    assert got["type_hints"] == {
        "record_id": "text",
        "email": "email-like",
        "amount": "numeric",
    }


def test_utf8_sig_and_blank_count():
    with tempfile.TemporaryDirectory() as directory:
        fixture = Path(directory) / "bom.csv"
        fixture.write_bytes("customer_id,city,note\n1001,Málaga,Café\n1002,東京,\n".encode("utf-8-sig"))
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(fixture)],
            check=True,
            capture_output=True,
            text=True,
        )
        got = json.loads(result.stdout)
        assert got["headers"] == ["customer_id", "city", "note"]
        assert got["blank_counts"]["note"] == 1
        assert got["duplicate_rows"] == 0
        with fixture.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        assert rows[0]["city"] == "Málaga"
        assert rows[0]["note"] == "Café"


def test_identifier_zeros_are_present_in_source_text():
    with (ROOT / "sample/leading-zero-ids.csv").open(
        newline="", encoding="utf-8-sig"
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert [row["sku"] for row in rows] == ["001234", "000742", "010010"]
    assert [row["postal_code"] for row in rows] == ["02115", "94107", "10001"]


if __name__ == "__main__":
    test_trimmed_full_row_duplicate()
    test_utf8_sig_and_blank_count()
    test_identifier_zeros_are_present_in_source_text()
    print("3 diagnostic fixture tests passed")
