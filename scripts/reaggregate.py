#!/usr/bin/env python3
"""
Re-build data/aggregated_records.csv from all JSON files on disk in
data/raw_search_results/.

Used after running the search_runner in multiple non-merging passes
(each pass overwrites the aggregated CSV). This script is idempotent.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW_DIR = REPO / "data" / "raw_search_results"
AGG_PATH = REPO / "data" / "aggregated_records.csv"


def main() -> int:
    if not RAW_DIR.exists():
        print(f"ERROR: {RAW_DIR} missing", file=sys.stderr)
        return 1
    fieldnames = [
        "id", "doi", "title", "abstract", "year",
        "authors", "journal", "source_db", "source_query",
    ]
    n = 0
    with AGG_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for db_dir in sorted(RAW_DIR.iterdir()):
            if not db_dir.is_dir():
                continue
            for jf in sorted(db_dir.glob("*.json")):
                try:
                    rows = json.loads(jf.read_text())
                except json.JSONDecodeError:
                    continue
                for r in rows:
                    w.writerow({k: (r.get(k, "") or "") for k in fieldnames})
                    n += 1
    print(f"[reaggregate] Wrote {n} rows to {AGG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
