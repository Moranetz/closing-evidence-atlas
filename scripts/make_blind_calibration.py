#!/usr/bin/env python3
"""
Create a blinded copy of calibration_sample.csv for Marion's independent
screening. Same 100 records, empty decision columns.

After Marion screens, her file is named calibration_sample_marion.csv and
sits alongside the LLM-screened calibration_sample.csv. Then
`scripts/compute_kappa.py` computes Cohen's κ between the two.

Stdlib only.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "search" / "calibration_sample.csv"
TARGET = REPO / "search" / "calibration_sample_blind.csv"


def main() -> int:
    if not SOURCE.exists():
        print(f"ERROR: {SOURCE} missing", file=sys.stderr)
        return 1
    with SOURCE.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []
    blank = {"decision": "", "decision_reason": "", "screener": "marion", "decision_date": ""}
    for r in rows:
        for k, v in blank.items():
            if k in r:
                r[k] = v
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with TARGET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"[blind] Wrote {len(rows)} blinded records to {TARGET}")
    print("[blind] For each row, fill: decision (include/exclude/uncertain) + decision_reason.")
    print("[blind] When done, save as calibration_sample_marion.csv and run scripts/compute_kappa.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
