#!/usr/bin/env python3
"""Small, safe CSV diagnostic for deciding whether a cleanup is needed.

It never uploads data and prints values only from column names and aggregate counts.
It deliberately does not modify or export a cleaned file: production cleanup and
business-rule mapping are the paid part of the service.
"""
import argparse, csv, json, re
from collections import Counter
from pathlib import Path

def diagnose(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        headers=list(reader.fieldnames or [])
        if not headers:
            raise ValueError('CSV has no header row')
        rows=[]
        for row in reader:
            # DictReader uses None for surplus fields; ignore them in the
            # aggregate report rather than exposing or crashing on values.
            rows.append({h: row.get(h) or '' for h in headers})
    blank={h:sum(1 for r in rows if not r[h].strip()) for h in headers}
    normalized=[tuple(r[h].strip() for h in headers) for r in rows]
    dup=sum(n-1 for n in Counter(normalized).values() if n>1)
    hints={}
    for h in headers:
        vals=[r[h].strip() for r in rows if r[h].strip()]
        if vals and all(re.fullmatch(r'-?\d+(\.\d+)?',v) for v in vals): hints[h]='numeric'
        elif vals and all(re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',v) for v in vals): hints[h]='email-like'
        else: hints[h]='text'
    return {'file':Path(path).name,'rows':len(rows),'columns':len(headers),'headers':headers,'blank_counts':blank,'duplicate_rows':dup,'type_hints':hints}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('csv_file'); args=p.parse_args(); print(json.dumps(diagnose(args.csv_file),ensure_ascii=False,indent=2))
