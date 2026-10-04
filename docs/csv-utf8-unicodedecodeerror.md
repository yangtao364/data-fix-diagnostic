# Fix a CSV UTF-8 or UnicodeDecodeError before cleaning data

A CSV can look normal in Excel and still fail in Python when it was exported as UTF-16, Windows-1252, or another encoding. This repository's diagnostic intentionally reads UTF-8 and UTF-8-with-BOM files through Python's utf-8-sig codec. It raises a decode error for incompatible bytes instead of guessing silently.

## Safe first step

Keep the original file unchanged. In Excel or your spreadsheet application, use Save As and choose CSV UTF-8. Then run the diagnostic against the converted copy:

```bash
python diagnose_csv.py converted/orders.csv
```

This avoids silently replacing characters in customer names, product titles, or SKU fields.

## Why guessing an encoding can damage data

A byte sequence may be valid under more than one encoding. A successful read is not proof that the text is correct. Check a few non-ASCII values after conversion, especially accents, Chinese characters, currency symbols, and smart punctuation.

## Other common causes

- The file is UTF-16 or Windows-1252 rather than UTF-8.
- A spreadsheet exported a tab-separated file with a .csv suffix.
- The file contains a byte-order mark or mixed encodings.
- A quoted field contains a line break or malformed quote.
- The file is empty or has no header row.

The diagnostic accepts a header row and reports aggregate structure; it does not rewrite the file or infer the correct business encoding.

## What to provide for a custom repair

Send a sanitized sample, the source application and export setting, the desired encoding, and a few expected non-ASCII values. Do not upload credentials or private customer data. For a clearly scoped conversion or cleanup delivered as CSV/Excel, use the [fixed-scope cleanup service on Fiverr](https://www.fiverr.com/awkrea/write-a-custom-python-automation-script-for-web-scraping-excel-and-data-tasks-fbfb).

## Related searches

This guide covers “CSV UnicodeDecodeError”, “Python CSV UTF-8”, “Excel CSV encoding”, and “Shopify CSV special characters”.
