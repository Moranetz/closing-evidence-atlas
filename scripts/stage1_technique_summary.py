#!/usr/bin/env python3
"""
Stage-1 by-technique summary: per-taxonomy-technique counts of included,
uncertain, and excluded records, plus the empirical-foundation deserts
(techniques with zero or very few included studies — direct RQ-5 evidence).

Outputs:
  results/stage1_by_technique.csv — per-technique counts + Stage-1 survivor flag
  results/stage1_survivor_report.md — human-readable summary in Persuasion-Max voice
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
TAXONOMY_PATH = REPO / "taxonomy" / "techniques.md"
OUTPUT_CSV = REPO / "results" / "stage1_by_technique.csv"
OUTPUT_REPORT = REPO / "results" / "stage1_survivor_report.md"

STAGE1_SURVIVOR_THRESHOLD = 5  # Atlas PROTOCOL § 9.7 C1: ≥ 5 eligible primary studies


def parse_taxonomy(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    pattern = re.compile(
        r"^###\s+`([a-z0-9\-]+)`\s+—\s+(.+?)\s*$",
        re.MULTILINE,
    )
    blocks = list(pattern.finditer(text))
    for i, m in enumerate(blocks):
        tid = m.group(1).strip()
        canonical = m.group(2).strip()
        block_start = m.end()
        block_end = blocks[i + 1].start() if i + 1 < len(blocks) else len(text)
        block = text[block_start:block_end]
        cluster_m = re.search(r"\*\*Cluster:\*\*\s+(.+?)$", block, re.MULTILINE)
        prior_m = re.search(r"\*\*Empirical status \(prior\):\*\*\s+(.+?)$", block, re.MULTILINE)
        entries.append({
            "taxonomy_id": tid,
            "canonical": canonical,
            "cluster": (cluster_m.group(1).strip() if cluster_m else "unknown"),
            "prior_status": (prior_m.group(1).strip() if prior_m else "unknown"),
        })
    return entries


def main() -> int:
    techs = parse_taxonomy(TAXONOMY_PATH)
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Count includes/uncertains/excludes per technique
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"include": 0, "uncertain": 0, "exclude": 0})
    for r in rows:
        decision = (r.get("decision") or "").strip()
        if decision not in ("include", "uncertain", "exclude"):
            continue
        for t in (r.get("provenance_techniques") or "").split(";"):
            t = t.strip()
            if t:
                counts[t][decision] += 1

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "taxonomy_id", "canonical", "cluster", "prior_status",
        "n_include", "n_uncertain", "n_exclude",
        "n_total_screened",
        "include_rate_pct",
        "stage1_survivor",
        "survivor_status",
    ]
    written: list[dict[str, str]] = []
    for t in techs:
        tid = t["taxonomy_id"]
        c = counts[tid]
        total = c["include"] + c["uncertain"] + c["exclude"]
        include_rate = (100 * c["include"] / total) if total > 0 else 0.0
        survivor = c["include"] >= STAGE1_SURVIVOR_THRESHOLD
        if c["include"] == 0:
            status = "DESERT (no eligible studies)"
        elif c["include"] < STAGE1_SURVIVOR_THRESHOLD:
            status = "FRAGILE (< 5 studies)"
        elif c["include"] < 20:
            status = "MODEST EVIDENCE"
        elif c["include"] < 50:
            status = "STRONG EVIDENCE"
        else:
            status = "DOMINANT LITERATURE"
        written.append({
            "taxonomy_id": tid,
            "canonical": t["canonical"],
            "cluster": t["cluster"],
            "prior_status": t["prior_status"],
            "n_include": str(c["include"]),
            "n_uncertain": str(c["uncertain"]),
            "n_exclude": str(c["exclude"]),
            "n_total_screened": str(total),
            "include_rate_pct": f"{include_rate:.1f}",
            "stage1_survivor": "yes" if survivor else "no",
            "survivor_status": status,
        })

    # Sort by include count descending
    written.sort(key=lambda r: (-int(r["n_include"]), r["taxonomy_id"]))
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(written)
    print(f"[stage1-summary] Wrote {len(written)} rows to {OUTPUT_CSV}")
    print()
    print(f"{'technique':<26} {'incl':>5} {'uncert':>6} {'excl':>6} {'total':>6}  status")
    print("-" * 90)
    for r in written:
        print(
            f"  {r['taxonomy_id']:<24} {r['n_include']:>5} "
            f"{r['n_uncertain']:>6} {r['n_exclude']:>6} {r['n_total_screened']:>6}  "
            f"{r['survivor_status']}"
        )

    # Build markdown report
    survivors = [r for r in written if r["stage1_survivor"] == "yes"]
    fragile = [r for r in written if r["survivor_status"] == "FRAGILE (< 5 studies)"]
    deserts = [r for r in written if r["survivor_status"] == "DESERT (no eligible studies)"]

    md = []
    md.append("# Stage-1 Survivor Report — Per-Technique Evidence Base")
    md.append("")
    md.append(
        "Auto-generated from `search/screening_stage1.csv` via "
        "`scripts/stage1_technique_summary.py`. Reflects screening state as of 2026-05-10."
    )
    md.append("")
    md.append("## Headline numbers")
    md.append("")
    md.append(f"- Techniques cataloged in taxonomy: **{len(written)}**")
    md.append(f"- Techniques with ≥ {STAGE1_SURVIVOR_THRESHOLD} Stage-1 included studies (survivors): **{len(survivors)}**")
    md.append(f"- Techniques with 1-{STAGE1_SURVIVOR_THRESHOLD-1} studies (FRAGILE): **{len(fragile)}**")
    md.append(f"- Techniques with 0 included studies (DESERT): **{len(deserts)}**")
    md.append("")
    md.append(
        "This is the empirical landscape of the sales-closing literature at Stage-1 screening. "
        "The DESERT and FRAGILE categories collectively are direct evidence for RQ-5: "
        "a meaningful fraction of named techniques in the practitioner literature have "
        "essentially no peer-reviewed empirical foundation."
    )
    md.append("")
    md.append("## Survivor techniques (≥ 5 Stage-1 includes)")
    md.append("")
    md.append("Ranked by include count. These techniques have enough primary literature to proceed to Stage-2 full-text screening and ultimately to per-technique Bayesian meta-analysis.")
    md.append("")
    md.append("| Technique | Cluster | Include | Uncertain | Exclude | Status |")
    md.append("| --- | --- | ---: | ---: | ---: | --- |")
    for r in survivors:
        md.append(
            f"| `{r['taxonomy_id']}` ({r['canonical']}) | {r['cluster']} | "
            f"{r['n_include']} | {r['n_uncertain']} | {r['n_exclude']} | {r['survivor_status']} |"
        )
    md.append("")
    md.append("## Fragile-evidence techniques (1-4 Stage-1 includes)")
    md.append("")
    md.append("These techniques have some empirical literature but below the pre-registered threshold for meta-analysis. They are reported descriptively in the final preprint with explicit caveats.")
    md.append("")
    md.append("| Technique | Cluster | Include | Uncertain | Exclude |")
    md.append("| --- | --- | ---: | ---: | ---: |")
    for r in fragile:
        md.append(
            f"| `{r['taxonomy_id']}` ({r['canonical']}) | {r['cluster']} | "
            f"{r['n_include']} | {r['n_uncertain']} | {r['n_exclude']} |"
        )
    md.append("")
    md.append("## Empirical deserts (0 Stage-1 includes)")
    md.append("")
    md.append("These techniques are named extensively in the practitioner literature (Hopkins, Voss, Sandler, MEDDIC, Challenger Sale) but did not surface in our systematic search of public-databases-only literature. This is direct evidence that they have **no peer-reviewed empirical foundation** at the level of our pre-registered inclusion criteria. Discussed in PROTOCOL.md § 2 RQ-5.")
    md.append("")
    md.append("| Technique | Cluster | Practitioner-claimed mechanism |")
    md.append("| --- | --- | --- |")
    for r in deserts:
        md.append(f"| `{r['taxonomy_id']}` ({r['canonical']}) | {r['cluster']} | per taxonomy |")
    md.append("")
    md.append("## Methodological notes")
    md.append("")
    md.append("- DESERT classification is conservative: it reflects only what surfaced from public-databases-only search. Per Deviation 001, paid databases (Scopus, Web of Science, PsycInfo, EBSCO) were not searched; some DESERT techniques may have evidence in those databases.")
    md.append("- The Stage-1 included count for each technique is an upper bound on what passes Stage-2 (full-text screening); expected drop is 60-80%.")
    md.append("- Per PROTOCOL.md § 9.7, the survivor classification at the final preprint stage requires Bayesian random-effects meta-analysis with multiverse robustness; this Stage-1 survivor count is the *eligibility threshold for that analysis*, not the analysis itself.")

    OUTPUT_REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n[stage1-summary] Wrote report to {OUTPUT_REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
