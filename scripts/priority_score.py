#!/usr/bin/env python3
"""
Priority-score each not-yet-screened record by likelihood of being an
in-scope persuasion/sales study.

Score components (all 0-1, weighted sum):
  - venue_tier: 1.0 if venue is a known behavioral / marketing / consumer
    psychology journal; 0.5 for general social-science / management; 0.0
    otherwise.
  - allowlist_density: fraction of behavioral allowlist tokens hitting the
    abstract+title.
  - methodology_signal: 1.0 if "experiment" / "randomi" / "field trial" /
    "intervention" in abstract+title.
  - provenance_multiplier: 1 + 0.3 × (provenance_count - 1), capped at 1.6.
  - source_penalty: 0.6× if source is arXiv or ClinicalTrials.gov (lower
    base rate of relevant records).

Records are sorted by score desc and the top N can be LLM-screened first.

Outputs: search/priority_scored.csv with `priority_score` column added.

Stdlib only.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
OUT_PATH = REPO / "search" / "priority_scored.csv"

# Tier 1 venues — top behavioral / marketing / consumer journals
TIER1_VENUE_TOKENS = [
    "journal of personality and social psychology",
    "journal of consumer research",
    "journal of marketing research",
    "journal of marketing",
    "marketing science",
    "journal of consumer psychology",
    "journal of experimental social psychology",
    "journal of experimental psychology",
    "personality and social psychology bulletin",
    "personality and social psychology review",
    "organizational behavior and human decision processes",
    "journal of applied psychology",
    "journal of personal selling",
    "psychological science",
    "journal of experimental political science",
    "psychological bulletin",
    "annual review of psychology",
    "journal of the academy of marketing science",
    "industrial marketing management",
    "judgment and decision making",
    "health communication",
    "communication research",
    "journal of communication",
    "journal of advertising",
    "advances in consumer research",
    "journal of behavioral decision making",
    "social influence",
    "social cognition",
    "european journal of social psychology",
    "british journal of social psychology",
    "basic and applied social psychology",
    "current directions in psychological science",
]

# Tier 2 — general social science / management / behavioral
TIER2_VENUE_TOKENS = [
    "management science",
    "journal of management",
    "strategic management journal",
    "psychology of",
    "social psychology",
    "behavioral science",
    "psychology and",
    "journal of social",
    "annual review of",
    "behavior research methods",
    "negotiation journal",
    "psyc",  # catch-all psyc-prefixed
    "social science research",
    "journal of political marketing",
    "transfusion",  # blood-donor literature
    "social psychological",
    "consumer behavior",
    "consumer behaviour",
    "marketing letters",
    "journal of business",
    "journal of retailing",
]

ALLOWLIST_TOKENS = [
    "compliance", "comply", "persuad", "persuas",
    "consumer", "customer", "buyer", "shopper",
    "donat", "marketing", "advertis", "purchas", "buying",
    "willingness to pay", "willingness to buy",
    "framing", "loss avers", "gain frame", "loss frame",
    "negotiat", "bargain",
    "social proof", "scarcity claim", "reciprocity",
    "anchor", "foot-in-the-door", "door-in-the-face",
    "low-ball", "lowball",
    "behavior chang", "behaviour chang",
    "compliance rate", "request",
]

METHODOLOGY_TOKENS = [
    "experiment", "experimental",
    "randomi", "rct",
    "field experiment", "field trial",
    "intervention",
    "manipulation",
    "between-subjects", "within-subjects",
    "controlled trial",
    "regression discontinuity", "instrumental variable",
    "difference-in-differences",
]


def venue_score(journal: str) -> float:
    j = journal.lower()
    for t in TIER1_VENUE_TOKENS:
        if t in j:
            return 1.0
    for t in TIER2_VENUE_TOKENS:
        if t in j:
            return 0.5
    return 0.0


def allowlist_density(text: str) -> float:
    text_low = text.lower()
    hits = sum(1 for t in ALLOWLIST_TOKENS if t in text_low)
    return min(hits / 4.0, 1.0)  # 4+ hits = full credit


def methodology_signal(text: str) -> float:
    text_low = text.lower()
    return 1.0 if any(t in text_low for t in METHODOLOGY_TOKENS) else 0.0


def provenance_multiplier(prov_count_str: str) -> float:
    try:
        n = int(prov_count_str or "1")
    except ValueError:
        n = 1
    return min(1.0 + 0.3 * (n - 1), 1.6)


def source_penalty(source_db: str) -> float:
    if source_db in ("arxiv", "clinicaltrials"):
        return 0.6
    return 1.0


def score_record(row: dict[str, str]) -> float:
    title = row.get("title", "")
    abstract = row.get("abstract", "")
    journal = row.get("journal", "")
    source_db = row.get("source_db", "")
    text = f"{title} {abstract}"
    v = venue_score(journal)
    a = allowlist_density(text)
    m = methodology_signal(text)
    base = 0.4 * v + 0.35 * a + 0.25 * m
    base *= provenance_multiplier(row.get("provenance_count", "1"))
    base *= source_penalty(source_db)
    return base


def main() -> int:
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []
    pending = [r for r in rows if not (r.get("decision") or "").strip()]
    print(f"[priority] Scoring {len(pending)} pending records...")
    scored = []
    for r in pending:
        s = score_record(r)
        r2 = dict(r)
        r2["priority_score"] = f"{s:.4f}"
        scored.append((s, r2))
    scored.sort(key=lambda x: -x[0])
    # Write priority-sorted CSV
    out_fields = fields + ["priority_score"]
    with OUT_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        for _, r in scored:
            w.writerow({k: r.get(k, "") for k in out_fields})
    # Summary
    bins = {"≥0.7": 0, "0.5-0.7": 0, "0.3-0.5": 0, "0.1-0.3": 0, "<0.1": 0}
    for s, _ in scored:
        if s >= 0.7:
            bins["≥0.7"] += 1
        elif s >= 0.5:
            bins["0.5-0.7"] += 1
        elif s >= 0.3:
            bins["0.3-0.5"] += 1
        elif s >= 0.1:
            bins["0.1-0.3"] += 1
        else:
            bins["<0.1"] += 1
    print(f"[priority] Wrote {len(scored)} scored records to {OUT_PATH}")
    print(f"[priority] Score distribution:")
    for k, v in bins.items():
        print(f"           {k}: {v}")
    print()
    print("[priority] Top 10 by priority:")
    for s, r in scored[:10]:
        print(f"  {s:.3f} | {r.get('year', '')} | {r.get('journal', '')[:50]} | {r.get('title', '')[:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
