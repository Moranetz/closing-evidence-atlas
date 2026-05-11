#!/usr/bin/env python3
"""
Apply individualized screening decisions from _priority_batch_1_decisions.json
(or another priority-batch decisions file) to the master screening CSV.

Matches by `i` field which indexes into the priority-sorted records list.

Stdlib only.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
PRIORITY_PATH = REPO / "search" / "priority_scored.csv"
DEFAULT_DECISIONS = REPO / "search" / "_priority_batch_1_decisions.json"


def main() -> int:
    decisions_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DECISIONS
    payload = json.loads(decisions_path.read_text())
    screener = payload.get("screener", "unknown")
    date = payload.get("decision_date", "")
    by_index = {d["i"]: d for d in payload.get("decisions", [])}

    # Load priority_scored to map index → record id
    with PRIORITY_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    id_to_decision: dict[str, dict] = {}
    for i in by_index:
        if i < len(rows):
            id_to_decision[rows[i]["id"]] = {
                "decision": by_index[i]["decision"],
                "decision_reason": by_index[i]["reason"],
                "screener": screener,
                "decision_date": date,
            }

    # Update master screening CSV
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        master_rows = list(csv.DictReader(f))
        fields = list(master_rows[0].keys()) if master_rows else []
    matched = 0
    overwrites = 0
    for r in master_rows:
        if r["id"] in id_to_decision:
            if (r.get("decision") or "").strip():
                overwrites += 1
            r.update(id_to_decision[r["id"]])
            matched += 1
    with SCREENING_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(master_rows)

    counts = Counter(d["decision"] for d in by_index.values())
    print(f"[apply] Matched {matched} records (overwrote {overwrites} prior decisions)")
    print(f"[apply] Decision counts: {dict(counts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
