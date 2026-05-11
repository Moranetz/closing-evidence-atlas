#!/usr/bin/env python3
"""
Prepare unique-records.csv for Stage-1 (title-abstract) screening.

Produces:
  search/screening_stage1.csv — one row per unique record with empty
    `decision`, `decision_reason`, `screener`, `decision_date` columns.

The screening operations themselves run in a separate session (Phase 1.4 of
the Atlas plan), with LLM-assisted re-screen + human calibration per
PROTOCOL.md § 13.2.

Stdlib only.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UNIQUE_PATH = REPO / "data" / "unique_records.csv"
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"


def main() -> int:
    if not UNIQUE_PATH.exists():
        print(f"ERROR: {UNIQUE_PATH} missing — run scripts/deduplicate.py first.", file=sys.stderr)
        return 1
    with UNIQUE_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    SCREENING_PATH.parent.mkdir(parents=True, exist_ok=True)
    out_fields = [
        "id", "doi", "title", "year", "authors", "journal",
        "abstract", "provenance_databases", "provenance_techniques",
        "provenance_count",
        # Screening decision fields:
        "decision",            # include / exclude / uncertain
        "decision_reason",     # short text from criteria
        "screener",            # human / llm-claude / llm-gpt / consensus
        "decision_date",       # YYYY-MM-DD
        "calibration_set",     # 1 if in calibration sample, else 0
    ]
    with SCREENING_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        for r in rows:
            row = {k: r.get(k, "") for k in out_fields if k in r}
            for k in ("decision", "decision_reason", "screener", "decision_date", "calibration_set"):
                row.setdefault(k, "")
            w.writerow(row)
    print(f"[screening] Wrote {len(rows)} rows to {SCREENING_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
