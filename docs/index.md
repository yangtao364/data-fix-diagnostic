# CSV and Excel data repair guides

Practical, local-first guides for diagnosing ecommerce CSV and Excel problems before cleanup or import.

## Guides

- [Remove duplicate rows from a CSV with Python](remove-duplicate-rows-from-csv.md)
- [Fix a CSV UTF-8 or UnicodeDecodeError](csv-utf8-unicodedecodeerror.md)

## Free diagnostic

Run the [local CSV diagnostic](../README.md) against a sanitized sample. It reports row counts, blank values, duplicate full rows, and conservative type hints without uploading the file.

## Fixed-scope help

If you need a cleaned file delivered, use the [public Fiverr cleanup service](https://www.fiverr.com/awkrea/write-a-custom-python-automation-script-for-web-scraping-excel-and-data-tasks-fbfb). Include the input format, the exact transformation rule, the expected output, and a sanitized sample. Never send credentials.

These guides explain safe, reproducible checks. They do not promise that a generic script can infer business rules or repair production data without review.
