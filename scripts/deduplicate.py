#!/usr/bin/env python3
"""
Deduplicate aggregated search results into a unique-record set.

Strategy (per PROTOCOL.md § 8):
1. Group by lowercased DOI when present.
2. For records without DOI, fuzzy-match on (normalized title, year, first author surname).
3. Pick canonical record per group: prefer record with longest abstract, then
   record with most non-empty fields.
4. Retain full provenance (which databases × techniques surfaced the record).

Stdlib only. Python 3.9+.

Outputs:
  data/unique_records.csv       — deduped records with provenance lists
  search/dedup_summary.json     — pre/post counts, dedup ratios per source
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
AGG_PATH = REPO / "data" / "aggregated_records.csv"
UNIQUE_PATH = REPO / "data" / "unique_records.csv"
SUMMARY_PATH = REPO / "search" / "dedup_summary.json"


def normalize_title(t: str) -> str:
    """Aggressive title normalization for fuzzy match."""
    t = t.lower()
    t = re.sub(r"<[^>]+>", " ", t)  # strip HTML tags
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def first_author_surname(authors: str) -> str:
    if not authors:
        return ""
    first = authors.split(",")[0].strip()
    # "First Last" or "Last, First" — take last token
    parts = first.split()
    if not parts:
        return ""
    return parts[-1].lower()


def normalize_doi(d: str) -> str:
    return d.lower().strip().replace("https://doi.org/", "").replace("http://doi.org/", "").rstrip("/")


def load_records(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def group_records(records: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    """Group by DOI when present, else by (norm_title, year, first_author_surname)."""
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in records:
        doi = normalize_doi(r.get("doi", ""))
        if doi:
            key = f"doi::{doi}"
        else:
            key = (
                f"sig::{normalize_title(r.get('title', ''))}"
                f"||{r.get('year', '').strip()}"
                f"||{first_author_surname(r.get('authors', ''))}"
            )
        groups[key].append(r)
    return groups


def pick_canonical(group: list[dict[str, str]]) -> dict[str, Any]:
    """Choose the record with the longest abstract; tie-break on field completeness."""
    def score(r: dict[str, str]) -> tuple[int, int]:
        abs_len = len(r.get("abstract", "") or "")
        non_empty = sum(1 for v in r.values() if v and v.strip())
        return (abs_len, non_empty)

    canonical = max(group, key=score).copy()
    # Build provenance lists across the group
    seen_db: list[str] = []
    seen_q: list[str] = []
    for r in group:
        db = (r.get("source_db") or "").strip()
        q = (r.get("source_query") or "").strip()
        if db and db not in seen_db:
            seen_db.append(db)
        if q and q not in seen_q:
            seen_q.append(q)
    canonical["provenance_databases"] = ";".join(seen_db)
    canonical["provenance_techniques"] = ";".join(seen_q)
    canonical["provenance_count"] = str(len(group))
    return canonical


def main() -> int:
    if not AGG_PATH.exists():
        print(f"ERROR: {AGG_PATH} does not exist", file=sys.stderr)
        return 1
    records = load_records(AGG_PATH)
    print(f"[dedup] Loaded {len(records)} aggregated records", flush=True)

    # Per-source counts pre-dedup
    pre_counts: dict[str, int] = defaultdict(int)
    for r in records:
        pre_counts[r.get("source_db", "unknown")] += 1

    groups = group_records(records)
    print(f"[dedup] {len(groups)} unique groups after primary grouping", flush=True)

    unique = [pick_canonical(g) for g in groups.values()]

    # Sort: most-cross-referenced first, then year desc
    unique.sort(
        key=lambda r: (-int(r.get("provenance_count", "1") or "1"), -int(r.get("year") or "0")),
    )

    fieldnames = [
        "id", "doi", "title", "abstract", "year",
        "authors", "journal", "source_db", "source_query",
        "provenance_databases", "provenance_techniques", "provenance_count",
    ]
    UNIQUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with UNIQUE_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in unique:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    print(f"[dedup] Wrote {len(unique)} unique records to {UNIQUE_PATH}", flush=True)

    # Summary stats
    multi_source = sum(1 for r in unique if int(r.get("provenance_count", "1")) > 1)
    has_doi = sum(1 for r in unique if r.get("doi"))
    has_abstract = sum(1 for r in unique if (r.get("abstract") or "").strip())
    summary = {
        "input_records": len(records),
        "unique_records": len(unique),
        "dedup_ratio": round(len(records) / max(len(unique), 1), 2),
        "multi_source_records": multi_source,
        "with_doi": has_doi,
        "with_abstract": has_abstract,
        "pre_dedup_counts_by_db": dict(pre_counts),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[dedup] Summary saved to {SUMMARY_PATH}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
