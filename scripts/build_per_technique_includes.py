#!/usr/bin/env python3
"""
Build per-technique included-study CSVs — one file per survivor technique
containing the Stage-1 included records that have that technique in their
provenance_techniques.

These are the candidate sets for Phase 1.5 full-text screening per technique.
Output: results/by_technique/<taxonomy_id>.csv
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
OUTPUT_DIR = REPO / "results" / "by_technique"

FIELDS_OUT = [
    "id", "doi", "year", "title", "authors", "journal",
    "abstract",
    "provenance_techniques", "provenance_count",
    "decision", "decision_reason", "screener",
]


def main() -> int:
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    includes = [r for r in rows if r.get("decision") == "include"]

    by_technique: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in includes:
        for t in (r.get("provenance_techniques") or "").split(";"):
            t = t.strip()
            if t:
                by_technique[t].append(r)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for tid, recs in sorted(by_technique.items()):
        out = OUTPUT_DIR / f"{tid}.csv"
        recs_sorted = sorted(recs, key=lambda r: (r.get("year", "0"), r.get("id", "")))
        with out.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS_OUT)
            w.writeheader()
            for r in recs_sorted:
                w.writerow({k: r.get(k, "") for k in FIELDS_OUT})
        written += 1
    print(f"[per-tech] Wrote {written} per-technique CSVs to {OUTPUT_DIR}")
    print()
    print(f"{'technique':<26} {'records':>8}")
    for tid in sorted(by_technique.keys()):
        print(f"  {tid:<24} {len(by_technique[tid]):>8}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
