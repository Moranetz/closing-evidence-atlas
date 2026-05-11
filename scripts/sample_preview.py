#!/usr/bin/env python3
"""
Print a random sample of unique records for quality inspection.

Verifies that the search yielded relevant records before Phase 1.4 screening
begins. Run with `python3 scripts/sample_preview.py [N]` (default N=20).

Stdlib only.
"""

from __future__ import annotations

import csv
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UNIQUE_PATH = REPO / "data" / "unique_records.csv"


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    if not UNIQUE_PATH.exists():
        print(f"ERROR: {UNIQUE_PATH} missing — run scripts/deduplicate.py first.", file=sys.stderr)
        return 1
    with UNIQUE_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    random.seed(20260510)
    sample = random.sample(rows, min(n, len(rows)))
    for i, r in enumerate(sample, 1):
        title = (r.get("title") or "").strip()
        if len(title) > 120:
            title = title[:120] + "..."
        abstract = (r.get("abstract") or "").strip()
        if len(abstract) > 200:
            abstract = abstract[:200] + "..."
        techniques = r.get("provenance_techniques", "")
        dbs = r.get("provenance_databases", "")
        print(f"{i}. {r.get('year', '????')} — {title}")
        print(f"   Authors: {(r.get('authors') or '')[:100]}")
        print(f"   Journal: {r.get('journal', '')}")
        print(f"   DOI: {r.get('doi', '')}")
        print(f"   DBs: {dbs} | Techniques: {techniques}")
        if abstract:
            print(f"   Abstract: {abstract}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
