# Free CSV Diagnostic

A small local-only diagnostic for Excel/CSV cleanup triage. It reports aggregate structure and data-quality signals without uploading the file.

## Run

```bash
python diagnose_csv.py sample/orders.csv
```

The output includes:

- row and column counts
- blank-value counts per column
- duplicate-row count
- conservative type hints (`numeric`, `email-like`, `text`)

## Safe sample policy

Use a sanitized sample only. Remove passwords, API keys, cookies, payment information, private customer data, and production credentials. This tool does not bypass access controls or collect data from websites.

## Need a fixed-scope repair?

After running the diagnostic, use the service page for one clearly reproducible issue. Include the output, expected result, and a small sanitized sample. Do not send credentials.
