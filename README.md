# Free CSV Diagnostic

A small local-only diagnostic for Excel/CSV cleanup triage. It reports aggregate structure and data-quality signals without uploading the file.

This is a qualification tool, not a free cleaning service. It does not change
rows, infer business rules, join files, calculate profit, or produce an
import-ready output. Those steps depend on the store's rules and are the scope
of a paid, fixed-price repair.

## Run

```bash
python diagnose_csv.py sample/orders.csv
```

The output includes:

- row and column counts
- blank-value counts per column
- duplicate-row count
- conservative type hints (`numeric`, `email-like`, `text`)

It reads only the selected local file. A header row is required. Extra fields in
malformed rows are ignored in the aggregate report instead of being printed.

## Safe sample policy

Use a sanitized sample only. Remove passwords, API keys, cookies, payment information, private customer data, and production credentials. This tool does not bypass access controls or collect data from websites.

## What the paid service adds

For a real dataset, a paid repair can include an agreed transformation plan,
cross-file joins, deduplication rules, field normalization, validation checks,
and delivery in the client's requested Excel/CSV or import format. The client
keeps control of credentials and should share a sanitized sample first.

## Need a fixed-scope repair?

If the report shows a problem, request a fixed-scope quote from the service
page. Include the output, expected result, and a small sanitized sample. Do not
send credentials. The free report helps confirm fit; it is not the deliverable.
