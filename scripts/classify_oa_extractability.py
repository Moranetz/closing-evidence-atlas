#!/usr/bin/env python3
"""
Classify OA records by *actual* extractability confidence based on publisher
prefix, OA URL host, and observed Phase 2 hit-rate.

The motivation is the methodological finding from Phase 2 expansion v2:
Unpaywall's `is_oa=true` flag does NOT guarantee a Phase 2 extractor can
actually pull a clean primary-study effect size from the paper. Some
publishers (Wiley, Elsevier, OUP) frequently report is_oa=true for paywalled
landing pages with publisher-side OA gates that block automated access.
Other publishers (Frontiers, MDPI, BMC, PMC) consistently expose clean
HTML/PDF that an extractor can read.

This script classifies OA records into 4 confidence tiers:

  HIGH        — empirically clean: Phase 2 batches consistently extract from
                these. Targets first.
  MEDIUM      — mixed track record; abstract+metadata reliably available;
                full-text sometimes accessible. Target second.
  LOW         — is_oa=true but publisher-side paywalls frequently fire.
                Expect ~25-40% actual extractability. Target only when
                higher-tier supply is exhausted.
  UNKNOWN     — publisher prefix not yet classified. Treat as low until
                empirically observed.

The classification is rule-based on DOI prefix and OA URL host substring.
Hit-rate evidence is summarized inline based on the Phase 2 pilot extractions
through atlas-044 (committed in `data/extracted_studies_pilot.csv`).

Stdlib only.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OA_PATH = REPO / "data" / "oa_status.csv"
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
EXTRACTED_PATH = REPO / "data" / "extracted_studies_pilot.csv"
OUTPUT_CSV = REPO / "results" / "oa_extractability.csv"
OUTPUT_REPORT = REPO / "results" / "oa_extractability_report.md"


# DOI-prefix-based classification.
# Justified by Phase 2 expansion pilots (atlas-001 to atlas-044):
HIGH_DOI_PREFIXES = {
    # Publisher       :  rationale
    "10.3389": "Frontiers — clean HTML, 7/9 records in original pilot extracted cleanly",
    "10.3390": "MDPI — clean HTML, 4/4 extracted in v2 batch (10.3390/jtaer, info, ijerph, su)",
    "10.5334": "Ubiquity Press / IRSP — clean HTML, atlas-006 extracted cleanly",
    "10.1186": "BMC — clean HTML, atlas-036 extracted cleanly",
    "10.31234": "PsyArXiv preprint server — clean PDF download, atlas-044 extracted cleanly",
}

MEDIUM_DOI_PREFIXES = {
    "10.1037": "APA — institutional repos + PMC mirrors; 2/3 PMC extractions clean, 1 eScholarship maintenance hit; abstract-only common on institutional repos",
    "10.1145": "ACM — DL behind subscription but arXiv preprints sometimes available; atlas-032 extracted via arXiv preprint",
    "10.1007": "Springer — mixed; atlas-040 extracted cleanly from open chapter, atlas-042 extracted cleanly; but some chapters paywalled despite is_oa=true",
}

LOW_DOI_PREFIXES = {
    "10.1002": "Wiley — is_oa=true frequently masks publisher-side paywall; atlas-034 + atlas-038 + atlas-035 (HBE) all returned abstract-only or 402/403",
    "10.1016": "Elsevier / ScienceDirect — is_oa=true frequently masks paywall; atlas-021 + atlas-039 + atlas-043 + atlas-041 all returned abstract-only or paywalled",
    "10.1080": "Taylor & Francis — frequently paywalled despite is_oa=true; atlas-022 + atlas-038 returned abstract-only",
    "10.1086": "Chicago / OUP — paywalled; atlas-024 + atlas-030 + atlas-037 (originally) returned paywalled",
    "10.1509": "AMA / Marketing journals — frequently paywalled",
    "10.2224": "Sociometric Pub — Ingenta paywall on full-text",
    "10.4992": "J-Stage Japanese psych — abstract-only English; full text may not exist in EN",
}

# OA-URL host substrings that override DOI-prefix classification (positive override only).
# Records hosted at these hosts are HIGH-confidence regardless of DOI prefix.
HIGH_OA_URL_HOSTS = {
    "ncbi.nlm.nih.gov/pmc": "PubMed Central — clean HTML + JATS XML, atlas-014 + atlas-015 + atlas-036 + atlas-037 all extracted cleanly",
    "europepmc.org": "Europe PMC mirror — clean HTML+JATS",
    "frontiersin.org": "Frontiers direct",
    "mdpi.com": "MDPI direct",
    "osf.io": "OSF preprint server",
    "biorxiv.org": "bioRxiv preprint server",
    "psyarxiv.com": "PsyArXiv preprint server",
    "arxiv.org": "arXiv preprint server",
}


def classify(doi: str, oa_url: str) -> tuple[str, str]:
    """Return (tier, rationale) for one record."""
    doi = (doi or "").lower().strip()
    oa_url = (oa_url or "").lower().strip()

    # Positive override: clean-host URL wins
    for host, rationale in HIGH_OA_URL_HOSTS.items():
        if host in oa_url:
            return "HIGH", rationale

    prefix = doi.split("/")[0] if "/" in doi else ""
    if prefix in HIGH_DOI_PREFIXES:
        return "HIGH", HIGH_DOI_PREFIXES[prefix]
    if prefix in MEDIUM_DOI_PREFIXES:
        return "MEDIUM", MEDIUM_DOI_PREFIXES[prefix]
    if prefix in LOW_DOI_PREFIXES:
        return "LOW", LOW_DOI_PREFIXES[prefix]
    return "UNKNOWN", f"DOI prefix {prefix} not in observed-publisher table"


def main() -> int:
    if not OA_PATH.exists():
        print(f"missing: {OA_PATH}", file=sys.stderr)
        return 1

    # Load already-extracted for cross-reference
    extracted = set()
    if EXTRACTED_PATH.exists():
        with EXTRACTED_PATH.open("r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["doi"]:
                    extracted.add(r["doi"].lower().strip())

    # Load Stage-1 inclusion decisions for per-record technique listings
    technique_by_doi: dict[str, str] = {}
    if SCREENING_PATH.exists():
        with SCREENING_PATH.open("r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["decision"] != "include":
                    continue
                doi = (r["doi"] or "").lower().strip()
                if doi:
                    technique_by_doi[doi] = r.get("provenance_techniques", "")

    rows_out = []
    tier_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
    extracted_by_tier = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}

    with OA_PATH.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            doi = (r.get("doi") or "").lower().strip()
            is_oa = (r.get("is_oa") or "").lower() == "true"
            oa_url = r.get("best_oa_pdf_url") or ""
            tier, rationale = classify(doi, oa_url)
            included_at_stage1 = doi in technique_by_doi
            already_extracted = doi in extracted

            rows_out.append({
                "doi": doi,
                "title": r.get("title", ""),
                "is_oa": is_oa,
                "oa_url": oa_url,
                "stage1_included": included_at_stage1,
                "techniques": technique_by_doi.get(doi, ""),
                "already_extracted": already_extracted,
                "extractability_tier": tier,
                "rationale": rationale,
            })

            # Tally only Stage-1 includes that are OA-true and not yet extracted
            if is_oa and included_at_stage1 and not already_extracted:
                tier_counts[tier] += 1
            if already_extracted:
                extracted_by_tier[tier] += 1

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)

    # Write summary report
    report_lines = [
        "# OA Extractability — classifier output",
        "",
        "Generated by `scripts/classify_oa_extractability.py`. Classifies every record in `data/oa_status.csv` by the likely actual extractability of its OA URL, based on DOI prefix and OA URL host.",
        "",
        "## Tier definitions",
        "",
        "- **HIGH** — publisher consistently exposes clean HTML/PDF to Phase 2 extractors. Target first.",
        "- **MEDIUM** — mixed accessibility; usually has full text but sometimes abstract-only.",
        "- **LOW** — `is_oa=true` flag frequently misleading; publisher-side paywalls fire.",
        "- **UNKNOWN** — publisher prefix not yet classified; treat as LOW until observed.",
        "",
        "## Headline numbers",
        "",
        "Total OA-true Stage-1-included records not yet extracted, by tier:",
        "",
        "| Tier | Count |",
        "| --- | ---: |",
        f"| HIGH | {tier_counts['HIGH']} |",
        f"| MEDIUM | {tier_counts['MEDIUM']} |",
        f"| LOW | {tier_counts['LOW']} |",
        f"| UNKNOWN | {tier_counts['UNKNOWN']} |",
        "",
        "Already-extracted records by tier (for Phase 2 hit-rate calibration):",
        "",
        "| Tier | Already extracted |",
        "| --- | ---: |",
        f"| HIGH | {extracted_by_tier['HIGH']} |",
        f"| MEDIUM | {extracted_by_tier['MEDIUM']} |",
        f"| LOW | {extracted_by_tier['LOW']} |",
        f"| UNKNOWN | {extracted_by_tier['UNKNOWN']} |",
        "",
        "## Phase 2 prioritization recommendation",
        "",
        "Run HIGH-tier extractions before MEDIUM-tier before LOW-tier. The LOW-tier records should only be attempted after HIGH and MEDIUM are exhausted, and only with realistic expectations: a ~25-40% extraction yield observed in the Phase 2 expansion v2 batch.",
        "",
        "## Per-prefix rationale",
        "",
        "### HIGH-confidence publishers",
        "",
    ]
    for prefix, rationale in HIGH_DOI_PREFIXES.items():
        report_lines.append(f"- `{prefix}/` — {rationale}")
    report_lines += ["", "### HIGH-confidence URL hosts (override DOI prefix)", ""]
    for host, rationale in HIGH_OA_URL_HOSTS.items():
        report_lines.append(f"- `{host}` — {rationale}")
    report_lines += ["", "### MEDIUM-confidence publishers", ""]
    for prefix, rationale in MEDIUM_DOI_PREFIXES.items():
        report_lines.append(f"- `{prefix}/` — {rationale}")
    report_lines += ["", "### LOW-confidence publishers", ""]
    for prefix, rationale in LOW_DOI_PREFIXES.items():
        report_lines.append(f"- `{prefix}/` — {rationale}")
    report_lines += [
        "",
        "## How to use this",
        "",
        "Before spawning a Phase 2 extraction batch, filter candidates to `extractability_tier=HIGH` first. Only fall through to MEDIUM and LOW when HIGH is exhausted for the target technique. The published classification table above should be updated as new publishers are encountered.",
    ]

    with OUTPUT_REPORT.open("w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[classify-oa] Classified {len(rows_out)} records.")
    print(f"[classify-oa] Tier counts (OA-true Stage-1 included, not yet extracted):")
    for tier, n in tier_counts.items():
        print(f"  {tier}: {n}")
    print(f"[classify-oa] Wrote {OUTPUT_CSV}")
    print(f"[classify-oa] Wrote {OUTPUT_REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
