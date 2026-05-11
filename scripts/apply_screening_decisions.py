#!/usr/bin/env python3
"""
Apply screening decisions from a JSON decisions file to the master
search/screening_stage1.csv and to search/calibration_sample.csv.

Reads `search/_calibration_decisions.json` (or path passed as argv[1]),
matches by the index in `calibration_sample.csv`, and writes the
`decision`, `decision_reason`, `screener`, `decision_date` columns.

Stdlib only.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DECISIONS_PATH = REPO / "search" / "_calibration_decisions.json"
SAMPLE_PATH = REPO / "search" / "calibration_sample.csv"
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"


def main() -> int:
    decisions_file = Path(sys.argv[1]) if len(sys.argv) > 1 else DECISIONS_PATH
    if not decisions_file.exists():
        print(f"ERROR: {decisions_file} missing", file=sys.stderr)
        return 1
    payload = json.loads(decisions_file.read_text(encoding="utf-8"))
    screener = payload.get("screener", "unknown")
    date = payload.get("decision_date", "")
    decisions = {d["i"]: d for d in payload.get("decisions", [])}

    # Load calibration sample to map index → record id
    with SAMPLE_PATH.open("r", encoding="utf-8") as f:
        sample_rows = list(csv.DictReader(f))
        sample_fields = list(sample_rows[0].keys()) if sample_rows else []

    if len(sample_rows) != len(decisions):
        print(
            f"WARN: {len(sample_rows)} sample rows vs {len(decisions)} decisions",
            file=sys.stderr,
        )

    # Build id → decision map (id is the stable identifier across files)
    id_to_decision: dict[str, dict] = {}
    for i, r in enumerate(sample_rows):
        if i in decisions:
            d = decisions[i]
            id_to_decision[r["id"]] = {
                "decision": d["decision"],
                "decision_reason": d["reason"],
                "screener": screener,
                "decision_date": date,
            }

    # Update calibration_sample.csv in place
    for r in sample_rows:
        if r["id"] in id_to_decision:
            r.update(id_to_decision[r["id"]])
    with SAMPLE_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sample_fields)
        w.writeheader()
        w.writerows(sample_rows)
    print(f"[apply] Updated {len(id_to_decision)} rows in {SAMPLE_PATH.name}")

    # Update screening_stage1.csv master
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        master_rows = list(csv.DictReader(f))
        master_fields = list(master_rows[0].keys()) if master_rows else []
    matched = 0
    for r in master_rows:
        if r["id"] in id_to_decision:
            r.update(id_to_decision[r["id"]])
            matched += 1
    with SCREENING_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=master_fields)
        w.writeheader()
        w.writerows(master_rows)
    print(f"[apply] Updated {matched} rows in {SCREENING_PATH.name}")

    # Summary stats
    counts: dict[str, int] = {"include": 0, "exclude": 0, "uncertain": 0}
    for d in decisions.values():
        counts[d["decision"]] = counts.get(d["decision"], 0) + 1
    print(f"[apply] Decisions: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
