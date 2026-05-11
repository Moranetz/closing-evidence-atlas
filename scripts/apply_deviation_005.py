#!/usr/bin/env python3
"""
Apply Deviation 005 — mark records with priority_score < threshold as
`exclude (low-priority deferred)` on the master screening CSV.

Default threshold: 0.10 (matches PROTOCOL_DEVIATIONS.md § Deviation 005).
"""

from __future__ import annotations

import csv
import datetime
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
PRIORITY_PATH = REPO / "search" / "priority_scored.csv"

THRESHOLD = 0.10


def main() -> int:
    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else THRESHOLD

    # Build id → priority_score map from priority_scored.csv
    score_by_id: dict[str, float] = {}
    with PRIORITY_PATH.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                score_by_id[r["id"]] = float(r.get("priority_score", "0") or "0")
            except ValueError:
                pass

    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []

    today = datetime.date.today().isoformat()
    counts = Counter()
    for r in rows:
        if (r.get("decision") or "").strip():
            counts["skipped (already screened)"] += 1
            continue
        score = score_by_id.get(r["id"])
        if score is None:
            counts["no priority score"] += 1
            continue
        if score < threshold:
            r["decision"] = "exclude"
            r["decision_reason"] = (
                f"heuristic-deviation-005: low-priority deferred "
                f"(priority_score={score:.4f} < {threshold}); see PROTOCOL_DEVIATIONS.md"
            )
            r["screener"] = "heuristic-deviation-005"
            r["decision_date"] = today
            counts["excluded (deviation-005)"] += 1
        else:
            counts["above threshold (still pending LLM)"] += 1

    with SCREENING_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
