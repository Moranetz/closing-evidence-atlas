#!/usr/bin/env python3
"""
Fetch open-access status from Unpaywall for every Stage-1 included record
with a DOI. Determines which records are accessible for autonomous full-text
screening (Phase 1.5) without paywall navigation.

Unpaywall API: https://api.unpaywall.org/v2/<doi>?email=<email>
Free, polite-pool, 100k/day. Returns OA status, OA URL (PDF), license.

Output:
  data/oa_status.csv — per-DOI OA status with PDF URL where available
  results/phase15_accessibility_report.md — summary

Stdlib only. Python 3.9+.
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
OUTPUT_CSV = REPO / "data" / "oa_status.csv"
OUTPUT_REPORT = REPO / "results" / "phase15_accessibility_report.md"

EMAIL = "marzumm24@gmail.com"
USER_AGENT = f"closer-evidence-atlas/0.1 (research; mailto:{EMAIL})"
DELAY = 0.15  # seconds between calls (Unpaywall allows ~7/sec polite-pool)


def fetch_unpaywall(doi: str) -> dict | None:
    doi_clean = doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "").rstrip("/")
    if not doi_clean:
        return None
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi_clean)}?email={urllib.parse.quote(EMAIL)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"_status": "not_in_unpaywall"}
        if e.code == 429:
            time.sleep(5)
            return None
        return {"_status": f"http_{e.code}"}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def main() -> int:
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    includes = [r for r in rows if r.get("decision") == "include"]
    print(f"[oa] Processing {len(includes)} Stage-1 included records")

    out_rows: list[dict[str, str]] = []
    stats: dict[str, int] = {
        "gold": 0,
        "green": 0,
        "hybrid": 0,
        "bronze": 0,
        "closed": 0,
        "no_doi": 0,
        "not_in_unpaywall": 0,
        "error": 0,
    }
    for i, r in enumerate(includes, 1):
        doi = (r.get("doi") or "").strip()
        if not doi:
            stats["no_doi"] += 1
            out_rows.append({
                "id": r["id"],
                "doi": "",
                "title": (r.get("title") or "")[:120],
                "oa_status": "no_doi",
                "is_oa": "false",
                "best_oa_pdf_url": "",
                "license": "",
            })
            continue
        data = fetch_unpaywall(doi)
        time.sleep(DELAY)
        if data is None or data.get("_status", "").startswith("http_"):
            stats["error"] += 1
            out_rows.append({
                "id": r["id"], "doi": doi,
                "title": (r.get("title") or "")[:120],
                "oa_status": "error", "is_oa": "false",
                "best_oa_pdf_url": "", "license": "",
            })
            continue
        if data.get("_status") == "not_in_unpaywall":
            stats["not_in_unpaywall"] += 1
            out_rows.append({
                "id": r["id"], "doi": doi,
                "title": (r.get("title") or "")[:120],
                "oa_status": "not_in_unpaywall", "is_oa": "false",
                "best_oa_pdf_url": "", "license": "",
            })
            continue
        is_oa = data.get("is_oa", False)
        oa_status = data.get("oa_status", "closed") or "closed"
        best_oa = data.get("best_oa_location") or {}
        pdf_url = best_oa.get("url_for_pdf", "") or best_oa.get("url", "")
        license_str = best_oa.get("license", "") or ""
        stats[oa_status] = stats.get(oa_status, 0) + 1
        out_rows.append({
            "id": r["id"],
            "doi": doi,
            "title": (r.get("title") or "")[:120],
            "oa_status": oa_status,
            "is_oa": "true" if is_oa else "false",
            "best_oa_pdf_url": pdf_url,
            "license": license_str,
        })
        if i % 50 == 0:
            print(f"  [{i}/{len(includes)}] checkpoint")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["id", "doi", "title", "oa_status", "is_oa", "best_oa_pdf_url", "license"]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)
    print(f"[oa] Wrote {len(out_rows)} rows to {OUTPUT_CSV}")
    print()
    print("=== OA status breakdown ===")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k:24s}: {v}")

    # Build report
    n_oa = sum(1 for r in out_rows if r["is_oa"] == "true")
    n_with_pdf = sum(1 for r in out_rows if r["best_oa_pdf_url"])
    md = []
    md.append("# Phase 1.5 Accessibility Report — Stage-1 Included Records OA Status")
    md.append("")
    md.append("Auto-generated from `scripts/fetch_oa_status.py`. Determines which Stage-1 included records are open-access and therefore accessible for autonomous Phase 1.5 (full-text screening) and Phase 2 (extraction) without paywall navigation.")
    md.append("")
    md.append("## Headline numbers")
    md.append("")
    md.append(f"- Stage-1 included records: **{len(out_rows)}**")
    md.append(f"- Records with DOI: **{len(out_rows) - stats['no_doi']}** ({100*(len(out_rows)-stats['no_doi'])/max(len(out_rows),1):.1f}%)")
    md.append(f"- Records flagged open-access (is_oa = true): **{n_oa}** ({100*n_oa/max(len(out_rows),1):.1f}%)")
    md.append(f"- Records with retrievable PDF URL: **{n_with_pdf}** ({100*n_with_pdf/max(len(out_rows),1):.1f}%)")
    md.append("")
    md.append("## OA status breakdown")
    md.append("")
    md.append("| OA status | N | % |")
    md.append("| --- | ---: | ---: |")
    total = max(len(out_rows), 1)
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        md.append(f"| {k} | {v} | {100*v/total:.1f}% |")
    md.append("")
    md.append("**Status legend:**")
    md.append("- `gold` — published in fully OA journal under a permissive license.")
    md.append("- `green` — published toll-access but author-version freely available in a repository.")
    md.append("- `hybrid` — published toll-access in subscription journal but article-level OA license paid.")
    md.append("- `bronze` — freely readable on publisher site but no OA license.")
    md.append("- `closed` — paywalled, no OA version known.")
    md.append("- `not_in_unpaywall` — DOI not indexed by Unpaywall.")
    md.append("- `no_doi` — record has no DOI in the corpus (e.g., ClinicalTrials.gov records, some preprints).")
    md.append("")
    md.append("## Implications for Phase 1.5 + Phase 2")
    md.append("")
    md.append(f"- **{n_with_pdf} records** have a retrievable PDF URL and can be screened/extracted autonomously without external credentials.")
    md.append(f"- Remaining records require either (a) institutional library access by Mel, (b) author-correspondence requests, or (c) deferral with documented coverage caveat.")
    md.append("")
    md.append("## Next-session entry point")
    md.append("")
    md.append("- Phase 1.5 full-text screening can begin autonomously on the OA-PDF subset.")
    md.append("- Closed-access records can be screened on title + abstract + extracted-effect-size-from-metadata as a fallback, but full RoB assessment requires full text.")
    md.append("- Final preprint reports the OA-accessibility breakdown transparently as a methodological detail.")

    OUTPUT_REPORT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\n[oa] Wrote report to {OUTPUT_REPORT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
