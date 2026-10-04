# CSV and Excel Data Cleaning Diagnostic

A local-only Python tool to diagnose common CSV and Excel data problems before you clean or import them.

It helps you check:

- duplicate rows in CSV files
- blank values and inconsistent columns
- numeric, email-like, and text fields
- malformed rows and basic file structure
- whether a dataset is ready for a cleanup or import workflow

This is useful for Shopify product CSV imports, ecommerce order exports, inventory spreadsheets, lead lists, and other Excel/CSV files.

## Run the diagnostic

Requirements: Python 3.10+ and a CSV file with a header row.

```bash
python diagnose_csv.py sample/orders.csv
```

The script reads the selected local file and prints an aggregate report. It does not upload data, change rows, bypass access controls, or collect credentials.

## Example output from sample/orders.csv

```json
{
  "file": "orders.csv",
  "rows": 4,
  "columns": 4,
  "headers": ["order_id", "email", "amount", "status"],
  "blank_counts": {"order_id": 0, "email": 1, "amount": 0, "status": 0},
  "duplicate_rows": 1,
  "type_hints": {"order_id": "numeric", "email": "email-like", "amount": "numeric", "status": "text"}
}
```

Use only a sanitized sample. Remove passwords, API keys, cookies, payment information, private customer data, and production credentials.

## What this free tool does not do

The diagnostic does not infer business rules, join multiple files, calculate profit, rewrite an import file, repair formulas, scrape login-protected websites, bypass CAPTCHA, or deploy an automation. Those tasks require the store's rules and a reviewable output.

## Need the file repaired?

For one clearly defined CSV/Excel cleanup task, see the [fixed-scope cleanup service on Fiverr](https://www.fiverr.com/awkrea/write-a-custom-python-automation-script-for-web-scraping-excel-and-data-tasks-fbfb).

The paid service can include agreed deduplication rules, field normalization, cross-file joins, validation checks, and delivery in the requested Excel, CSV, or import format. Start with a sanitized sample and the expected result. Never send passwords or access tokens.

## Typical search problems

This repository is designed around real troubleshooting queries such as:

- how to remove duplicate rows from CSV
- how to clean inconsistent Excel columns
- how to merge CSV files with Python
- how to diagnose CSV encoding and Unicode errors
- how to prepare a Shopify CSV import
- how to validate an ecommerce inventory spreadsheet

## License

Use and modify this diagnostic for local data-quality checks. You are responsible for confirming that you have the right to process the data.


## Troubleshooting guides

See the [CSV and Excel data repair guides](docs/index.md) for reproducible pages on duplicate rows, UTF-8/UnicodeDecodeError, leading-zero identifiers, and safe cleanup boundaries.

To run the regression checks after cloning:

```bash
python tests/test_diagnostic.py
```
