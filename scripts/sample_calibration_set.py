#!/usr/bin/env python3
"""
Sample a stratified-random 100-record calibration set from
search/screening_stage1.csv and mark calibration_set=1 on the master CSV.

Stratification: weighted across techniques so each technique with ≥ 5
candidate records contributes proportionally; rare techniques (< 5 records)
contribute all their records.

Output: search/calibration_sample.csv — the 100 records prepped for screening.

Stdlib only.
"""

from __future__ import annotations

import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
SAMPLE_PATH = REPO / "search" / "calibration_sample.csv"

CALIBRATION_N = 100
SEED = 20260510


def main() -> int:
    if not SCREENING_PATH.exists():
        print(f"ERROR: {SCREENING_PATH} missing", file=sys.stderr)
        return 1
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    # Stratify by primary technique (first in provenance_techniques)
    by_tech: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        techs = (r.get("provenance_techniques", "") or "").split(";")
        primary = (techs[0] if techs else "").strip() or "unknown"
        by_tech[primary].append(i)

    rng = random.Random(SEED)
    sampled: list[int] = []
    # First: include all from techniques with < 5 records (rare-tech inclusion)
    rare_idx: list[int] = []
    main_pool: list[tuple[str, list[int]]] = []
    for tech, idxs in sorted(by_tech.items()):
        if len(idxs) < 5:
            rare_idx.extend(idxs)
        else:
            main_pool.append((tech, idxs))
    # Cap rare contributions at 25% of calibration N
    if len(rare_idx) > CALIBRATION_N // 4:
        rare_idx = rng.sample(rare_idx, CALIBRATION_N // 4)
    sampled.extend(rare_idx)

    remaining_needed = CALIBRATION_N - len(sampled)
    if remaining_needed > 0 and main_pool:
        # Proportional allocation across remaining techniques
        total_main = sum(len(idxs) for _, idxs in main_pool)
        allocated = 0
        for tech, idxs in main_pool:
            quota = round(remaining_needed * len(idxs) / total_main)
            quota = min(quota, len(idxs))
            sampled.extend(rng.sample(idxs, quota))
            allocated += quota
        # Fill any remaining gap from a global random pool
        if len(sampled) < CALIBRATION_N:
            avail = [i for i in range(len(rows)) if i not in sampled]
            extra_n = CALIBRATION_N - len(sampled)
            sampled.extend(rng.sample(avail, min(extra_n, len(avail))))

    sampled = sorted(set(sampled))[:CALIBRATION_N]
    print(f"[calib] Sampled {len(sampled)} records across "
          f"{len({rows[i].get('provenance_techniques', '').split(';')[0] for i in sampled})} techniques")

    # Mark calibration_set=1 on master
    for i in sampled:
        rows[i]["calibration_set"] = "1"
    with SCREENING_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Write calibration sample to its own file
    with SAMPLE_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for i in sampled:
            w.writerow(rows[i])
    print(f"[calib] Wrote {len(sampled)} rows to {SAMPLE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
