# Two synthetic, reproducible cases

These cases contain invented values only. They show how to read the diagnostic; they are not customer results or proof of a production cleanup.

## Case 1: a duplicate after trimming outer spaces

Fixture: [`sample/case-duplicate-whitespace.csv`](../sample/case-duplicate-whitespace.csv)

The second `A-100` row has one leading space in `record_id`. The diagnostic strips outer spaces before comparing full rows, so it reports one extra copy. It does not delete either row or decide whether the duplicate is valid.

Command:

```bash
python diagnose_csv.py sample/case-duplicate-whitespace.csv
```

Output generated from the current `diagnose_csv.py`:

```json
{
  "file": "case-duplicate-whitespace.csv",
  "rows": 3,
  "columns": 3,
  "headers": [
    "record_id",
    "email",
    "amount"
  ],
  "blank_counts": {
    "record_id": 0,
    "email": 0,
    "amount": 0
  },
  "duplicate_rows": 1,
  "type_hints": {
    "record_id": "text",
    "email": "email-like",
    "amount": "numeric"
  }
}
```

A reviewer should now inspect both source rows and decide whether `record_id` is the correct business key. If the rows represent two legitimate events, keep both.

## Case 2: identifier text with leading zeros

Fixture: [`sample/leading-zero-ids.csv`](../sample/leading-zero-ids.csv)

The `sku` and `postal_code` fields are identifiers written with leading zeros. The diagnostic reads them as strings and reports a simple `numeric` hint because the characters contain only digits. It does not convert, format, or export these values.

Command:

```bash
python diagnose_csv.py sample/leading-zero-ids.csv
```

Output generated from the current `diagnose_csv.py`:

```json
{
  "file": "leading-zero-ids.csv",
  "rows": 3,
  "columns": 3,
  "headers": [
    "sku",
    "postal_code",
    "amount"
  ],
  "blank_counts": {
    "sku": 0,
    "postal_code": 0,
    "amount": 0
  },
  "duplicate_rows": 0,
  "type_hints": {
    "sku": "numeric",
    "postal_code": "numeric",
    "amount": "numeric"
  }
}
```

Before opening the file in Excel, import the identifier columns as Text through **Data → From Text/CSV**. Compare the loaded values with the source text; a numeric hint in this report is not a recommendation to change the field.
