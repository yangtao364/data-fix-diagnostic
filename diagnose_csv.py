#!/usr/bin/env python3
"""Small, safe CSV diagnostic: reports schema, blank rates, duplicate rows, and type hints.
It never uploads data and prints values only from column names and aggregate counts.
"""
import argparse, csv, json, re
from collections import Counter
from pathlib import Path

def diagnose(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    headers=list(rows[0]) if rows else []
    blank={h:sum(1 for r in rows if not (r.get(h) or '').strip()) for h in headers}
    normalized=[tuple((r.get(h) or '').strip() for h in headers) for r in rows]
    dup=sum(n-1 for n in Counter(normalized).values() if n>1)
    hints={}
    for h in headers:
        vals=[(r.get(h) or '').strip() for r in rows if (r.get(h) or '').strip()]
        if vals and all(re.fullmatch(r'-?\d+(\.\d+)?',v) for v in vals): hints[h]='numeric'
        elif vals and all(re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',v) for v in vals): hints[h]='email-like'
        else: hints[h]='text'
    return {'file':Path(path).name,'rows':len(rows),'columns':len(headers),'headers':headers,'blank_counts':blank,'duplicate_rows':dup,'type_hints':hints}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('csv_file'); args=p.parse_args(); print(json.dumps(diagnose(args.csv_file),ensure_ascii=False,indent=2))
