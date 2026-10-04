# Keep leading zeros when Excel imports a CSV

A product code such as `001234`, postal code `02115`, or account ID `000742` is an identifier, even though it looks numeric. CSV stores characters; Excel may automatically interpret those characters as a number when a file is opened directly. That conversion can remove leading zeros, display a long identifier in scientific notation, or round values beyond Excel's numeric precision.

Microsoft recommends importing text data with Power Query and setting identifier columns to Text. See [Keeping leading zeros and large numbers](https://support.microsoft.com/en-us/excel/keeping-leading-zeros-and-large-numbers) for the supported workflow and the 15-significant-digit limitation.

## Import with a text type in Excel

1. Open a blank workbook. Do not double-click the CSV.
2. Select **Data → From Text/CSV**, choose the file, and confirm the delimiter and file origin in the preview.
3. Select **Transform Data** (or **Edit** in older builds) to open Power Query.
4. Select the identifier column, then choose **Transform → Data Type → Text**. Remove or replace an automatic “Changed Type” step if it converted the column first.
5. Check a few values that begin with `0` and any long identifiers in the preview.
6. Load to a new worksheet. Keep the original CSV as the source of record.

A custom number format changes display inside a workbook; it cannot restore zeros that were already removed during import. For identifiers that leave Excel, storing the column as Text is safer than formatting a numeric value.

## What this repository checks

The diagnostic accepts CSV only. It opens the file with `encoding='utf-8-sig'`, reads each declared header field as a string, and strips outer spaces for aggregate checks. A column containing only values such as `001234` receives the heuristic type hint `numeric` because its characters match a simple number pattern. That label does not convert or rewrite the values, and the script never exports an Excel workbook.

Run it before importing:

```bash
python diagnose_csv.py sample/leading-zero-ids.csv
```

The included fixture intentionally contains identifier-looking values and an amount column. The expected report is:

```json
{
  "file": "leading-zero-ids.csv",
  "rows": 3,
  "columns": 3,
  "headers": ["sku", "postal_code", "amount"],
  "blank_counts": {"sku": 0, "postal_code": 0, "amount": 0},
  "duplicate_rows": 0,
  "type_hints": {"sku": "numeric", "postal_code": "numeric", "amount": "numeric"}
}
```

Because the report intentionally prints aggregate metadata rather than cell values, verify the source text directly when a code's exact spelling matters. One safe, read-only check is:

```bash
python - <<'PY'
import csv
with open('sample/leading-zero-ids.csv', newline='', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        print(repr(row['sku']), repr(row['postal_code']))
PY
```

Expected output starts with `'001234' '02115'`; the quotes in `repr` make it clear that the values remain strings. Never paste passwords, payment data, or private customer records into a public issue or example.

## Before an import or repair

- Identify which columns are identifiers and which are quantities or amounts.
- Choose Text for IDs, SKUs, ZIP/postal codes, phone numbers, and other codes where spelling matters.
- Spot-check the loaded values against the original CSV.
- Export a test file and inspect its raw text before sending it to another system.
- If a production file was already opened and saved by Excel, compare it to the untouched source; zeros lost in that step cannot be inferred safely.

This diagnostic does not repair a damaged workbook, merge files, or validate a Shopify schema. For an agreed cleanup, send a sanitized sample and the expected output fields: [fixed-scope cleanup](https://www.fiverr.com/awkrea/write-a-custom-python-automation-script-for-web-scraping-excel-and-data-tasks-fbfb)
