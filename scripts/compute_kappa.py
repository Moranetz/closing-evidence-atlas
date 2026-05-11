#!/usr/bin/env python3
"""
Compute Cohen's κ between the LLM-screened calibration_sample.csv and
Marion's human-screened calibration_sample_marion.csv.

Two-rater agreement on the categorical `decision` column with categories
{include, exclude, uncertain}.

Reports:
  - Per-rater category counts
  - Observed agreement P_o
  - Chance agreement P_e
  - Cohen's κ
  - Per-category agreement breakdown
  - Disagreement list (id, both raters' decisions, both raters' reasons)

Acceptance threshold per PROTOCOL.md § 13: κ ≥ 0.70.

Stdlib only.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LLM_PATH = REPO / "search" / "calibration_sample.csv"
HUMAN_PATH = REPO / "search" / "calibration_sample_marion.csv"
REPORT_PATH = REPO / "search" / "calibration_kappa.md"

CATEGORIES = ["include", "exclude", "uncertain"]
KAPPA_THRESHOLD = 0.70


def load_decisions(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        print(f"ERROR: {path} missing", file=sys.stderr)
        sys.exit(1)
    out: dict[str, dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = (r.get("decision") or "").strip().lower()
            if d:
                out[r["id"]] = {
                    "decision": d,
                    "reason": r.get("decision_reason", ""),
                    "title": r.get("title", ""),
                }
    return out


def cohens_kappa(a: list[str], b: list[str], categories: list[str]) -> dict:
    n = len(a)
    if n == 0:
        return {"kappa": float("nan"), "p_o": 0.0, "p_e": 0.0, "n": 0}
    agree = sum(1 for x, y in zip(a, b) if x == y)
    p_o = agree / n
    counts_a = Counter(a)
    counts_b = Counter(b)
    p_e = sum((counts_a[c] / n) * (counts_b[c] / n) for c in categories)
    kappa = (p_o - p_e) / (1 - p_e) if (1 - p_e) > 0 else float("nan")
    return {"kappa": kappa, "p_o": p_o, "p_e": p_e, "n": n, "agree": agree}


def main() -> int:
    llm = load_decisions(LLM_PATH)
    human = load_decisions(HUMAN_PATH)
    common_ids = sorted(set(llm) & set(human))
    if not common_ids:
        print("ERROR: no common decided records between the two raters.", file=sys.stderr)
        return 1
    a = [llm[i]["decision"] for i in common_ids]
    b = [human[i]["decision"] for i in common_ids]
    stats = cohens_kappa(a, b, CATEGORIES)

    print(f"N decisions compared: {stats['n']}")
    print(f"Observed agreement P_o: {stats['p_o']:.3f}")
    print(f"Chance agreement P_e: {stats['p_e']:.3f}")
    print(f"Cohen's κ: {stats['kappa']:.3f}")
    print(f"Acceptance threshold: κ ≥ {KAPPA_THRESHOLD}")
    print(f"Status: {'PASS' if stats['kappa'] >= KAPPA_THRESHOLD else 'FAIL — criteria revision needed'}")
    print()

    # Per-category agreement matrix
    matrix: dict[str, Counter] = {c: Counter() for c in CATEGORIES}
    for x, y in zip(a, b):
        matrix[x][y] += 1
    print("Confusion matrix (rows = LLM, cols = Marion):")
    header = "                " + "  ".join(f"{c:>10s}" for c in CATEGORIES)
    print(header)
    for c in CATEGORIES:
        row = f"  LLM={c:<10s}" + "  ".join(f"{matrix[c][cc]:>10d}" for cc in CATEGORIES)
        print(row)
    print()

    # Disagreement list
    disagreements = [i for i, (x, y) in zip(common_ids, zip(a, b)) if x != y]
    print(f"Disagreements: {len(disagreements)}")
    for i in disagreements[:25]:
        print(f"  {i}")
        print(f"    title: {(llm[i]['title'] or '')[:90]}")
        print(f"    LLM: {llm[i]['decision']} — {llm[i]['reason']}")
        print(f"    Marion: {human[i]['decision']} — {human[i]['reason']}")
    if len(disagreements) > 25:
        print(f"  ... and {len(disagreements) - 25} more.")

    # Write report
    out: list[str] = []
    out.append("# Calibration κ Report")
    out.append("")
    out.append(f"- N: {stats['n']}")
    out.append(f"- Observed agreement: {stats['p_o']:.3f}")
    out.append(f"- Chance agreement: {stats['p_e']:.3f}")
    out.append(f"- Cohen's κ: **{stats['kappa']:.3f}**")
    out.append(f"- Threshold (PROTOCOL § 13): κ ≥ {KAPPA_THRESHOLD}")
    out.append(f"- Result: **{'PASS' if stats['kappa'] >= KAPPA_THRESHOLD else 'FAIL'}**")
    out.append("")
    out.append("## Confusion matrix (rows = LLM, cols = Marion)")
    out.append("")
    out.append("|       | include | exclude | uncertain |")
    out.append("| ----- | ------: | ------: | --------: |")
    for c in CATEGORIES:
        out.append(f"| LLM={c} | {matrix[c]['include']} | {matrix[c]['exclude']} | {matrix[c]['uncertain']} |")
    out.append("")
    out.append(f"## Disagreements ({len(disagreements)})")
    out.append("")
    for i in disagreements:
        out.append(f"### `{i}`")
        out.append(f"- Title: {llm[i]['title']}")
        out.append(f"- LLM: **{llm[i]['decision']}** — {llm[i]['reason']}")
        out.append(f"- Marion: **{human[i]['decision']}** — {human[i]['reason']}")
        out.append("")
    REPORT_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"\nReport saved to {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
