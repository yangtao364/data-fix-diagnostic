# Diagnose UTF-8 CSV errors safely

This guide explains what the local CSV diagnostic can and cannot tell you when a CSV file raises a UTF-8 error or opens with garbled characters.

The diagnostic is deliberately read-only. It never uploads the selected file, writes a replacement CSV, or prints row values.

## What the diagnostic expects

`diagnose_csv.py` opens the file as follows:

```python
open(path, newline="", encoding="utf-8-sig")
```

`utf-8-sig` accepts ordinary UTF-8 and UTF-8 with a leading UTF-8 byte-order mark (BOM). It does not detect or convert arbitrary encodings such as Windows-1252, Latin-1, UTF-16, or Shift-JIS. See the [Python codecs documentation](https://docs.python.org/3/library/codecs.html).

## Quick, safe diagnosis

Work from a copy or sanitized sample. Keep the original file unchanged.

```bash
python diagnose_csv.py /path/to/sample.csv
```

A UTF-8 problem normally appears as an uncaught `UnicodeDecodeError` and the command exits with status 1. An empty file raises `ValueError: CSV has no header row`.

### Validate UTF-8 without changing the file

```bash
python -c "from pathlib import Path; Path('/path/to/sample.csv').read_bytes().decode('utf-8-sig'); print('valid UTF-8 (BOM accepted if present)')"
```

Do not use `errors='ignore'` or `errors='replace'`; those options can silently discard or alter characters.

## Common symptoms

A `UnicodeDecodeError` commonly means the producer used UTF-16, Windows-1252, another legacy code page, or the file is damaged. Ask the producing system to export CSV UTF-8, or import through Excel's Text/CSV flow and choose the known source encoding.

If Excel displays mojibake but the diagnostic succeeds, import through **Data > Get Data > From File > From Text/CSV** and select the correct origin. See [Microsoft's UTF-8 CSV guidance](https://support.microsoft.com/en-us/excel/opening-csv-utf-8-files-correctly-in-excel).

A file that appears as one column usually has a delimiter or locale problem. This diagnostic uses Python's default comma-separated dialect; choose the actual delimiter in the import flow. See the [Python csv documentation](https://docs.python.org/3/library/csv.html).

## Limits

The report is not a business-readiness check. It does not auto-detect encodings, check dates or business rules, repair or export files, or infer the intended delimiter. Type hints are only `numeric`, `email-like`, or `text`. The script reads all rows into memory, so use a small sanitized sample for large exports.

Excel lists a maximum of 1,048,576 rows and 16,384 columns for worksheets. See [Microsoft's current limits](https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3).

## Remediation loop

1. Preserve the original export and make a sanitized working copy.
2. Run the diagnostic.
3. If it raises `UnicodeDecodeError`, confirm the source encoding and re-export as UTF-8; never overwrite the original.
4. If decoding succeeds but Excel displays mojibake, import through Text/CSV with UTF-8 (65001) or re-save as CSV UTF-8.
5. Rerun the diagnostic and separately verify delimiters and business rules.

For a reviewed conversion or cleanup after the encoding issue is understood, use the [fixed-scope cleanup service](https://www.fiverr.com/awkrea/write-a-custom-python-automation-script-for-web-scraping-excel-and-data-tasks-fbfb).