#!/usr/bin/env python3
"""
Atlas Phase 1 — public-database systematic search runner.

Hits PubMed, OpenAlex, Semantic Scholar, Crossref, arXiv, OSF Registries,
ClinicalTrials.gov for each technique in the taxonomy. Saves raw JSON per
(database, technique) and a normalized aggregated CSV.

Stdlib only. No pip install required. Python 3.9+.

Usage:
  python3 scripts/search_runner.py [--databases DB,DB,...] [--max-per-query N]

Reads taxonomy techniques from `taxonomy/techniques.md` (parses the
`taxonomy_id` and aliases sections).

Outputs:
  data/raw_search_results/<database>/<technique_id>.json  — raw responses
  data/aggregated_records.csv                              — normalized rows
  search/search_log.md                                     — per-DB stats
"""

from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parent.parent
RAW_DIR = REPO / "data" / "raw_search_results"
AGG_PATH = REPO / "data" / "aggregated_records.csv"
LOG_PATH = REPO / "search" / "search_log.md"
TAXONOMY_PATH = REPO / "taxonomy" / "techniques.md"

USER_AGENT = "closer-evidence-atlas/0.1 (research; mailto:marzumm24@gmail.com)"

# Generic context terms layered into every per-technique query.
CONTEXT_TERMS = [
    "sales", "compliance", "consumer", "persuasion",
    "negotiation", "buyer", "marketing", "purchase",
]

DEFAULT_DATABASES = [
    "pubmed", "openalex", "semantic_scholar", "crossref",
    "arxiv", "osf_registrations", "clinicaltrials",
]


# ---------------------------------------------------------------------------
# Taxonomy parser
# ---------------------------------------------------------------------------

def parse_taxonomy(path: Path) -> list[dict[str, Any]]:
    """Parse `taxonomy/techniques.md` into a list of {id, canonical, aliases}."""
    text = path.read_text(encoding="utf-8")
    entries: list[dict[str, Any]] = []
    # Each technique block starts with `### \`<id>\` — Canonical Name`
    pattern = re.compile(
        r"^###\s+`([a-z0-9\-]+)`\s+—\s+(.+?)\s*$",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        tid = m.group(1).strip()
        canonical = m.group(2).strip()
        block_start = m.end()
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[block_start:block_end]
        aliases = []
        # Aliases line format: `- **Aliases:** FITD; gradual commitment; ...`
        alias_match = re.search(
            r"\*\*Aliases:\*\*\s+(.+?)$",
            block,
            re.MULTILINE,
        )
        if alias_match:
            raw = alias_match.group(1)
            for piece in re.split(r";|/|,", raw):
                piece = piece.strip()
                if piece and piece.lower() != "aliases":
                    aliases.append(piece)
        entries.append(
            {
                "taxonomy_id": tid,
                "canonical": canonical,
                "aliases": aliases,
            }
        )
    return entries


def technique_terms(t: dict[str, Any]) -> list[str]:
    """Return phrase-search terms for one technique (canonical + aliases).

    Includes hyphen-stripped variants because some databases (notably PubMed)
    treat hyphens as exact-match characters, missing many records.
    """
    terms: list[str] = [t["canonical"], *t["aliases"]]
    # Add hyphen-stripped variants
    extra: list[str] = []
    for term in terms:
        if "-" in term:
            extra.append(term.replace("-", " "))
    terms.extend(extra)
    # Dedup case-insensitively, drop very short
    seen = set()
    out: list[str] = []
    for term in terms:
        low = re.sub(r"\s+", " ", term.lower().strip())
        if len(low) < 3 or low in seen:
            continue
        seen.add(low)
        out.append(term.strip())
    return out


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def http_get(
    url: str,
    *,
    accept: str = "application/json",
    timeout: int = 30,
    max_retries: int = 4,
) -> bytes:
    """GET with exponential-backoff retry on 429/5xx and transient network errors."""
    last_err: Exception | None = None
    for attempt in range(max_retries):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": accept,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504):
                wait = (2 ** attempt) * 3  # 3, 6, 12, 24 seconds
                time.sleep(wait)
                continue
            raise RuntimeError(f"HTTP {e.code} for {url}: {e.read()[:300]!r}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            wait = (2 ** attempt) * 2
            time.sleep(wait)
            continue
    raise RuntimeError(f"Exhausted retries for {url}: {last_err}")


# ---------------------------------------------------------------------------
# Per-database searchers
# Each returns list of {id, doi, title, abstract, year, authors, source_db, source_query}
# ---------------------------------------------------------------------------

def search_pubmed(technique: dict[str, Any], max_results: int = 200) -> list[dict[str, Any]]:
    terms = technique_terms(technique)
    tech_block = " OR ".join(f'"{t}"[tiab]' for t in terms)
    ctx_block = " OR ".join(f'"{c}"[tiab]' for c in CONTEXT_TERMS)
    query = f"({tech_block}) AND ({ctx_block})"
    enc = urllib.parse.quote(query)
    url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=pubmed&term={enc}&retmax={max_results}&retmode=json"
    )
    body = http_get(url)
    data = json.loads(body.decode("utf-8"))
    pmids = data.get("esearchresult", {}).get("idlist", [])
    if not pmids:
        return []
    # esummary in chunks of 100
    out: list[dict[str, Any]] = []
    for chunk_start in range(0, len(pmids), 100):
        chunk = pmids[chunk_start:chunk_start + 100]
        ids = ",".join(chunk)
        url2 = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            f"?db=pubmed&id={ids}&retmode=json"
        )
        body2 = http_get(url2)
        time.sleep(0.4)  # rate-limit
        sums = json.loads(body2.decode("utf-8")).get("result", {})
        for pid in chunk:
            r = sums.get(pid)
            if not r:
                continue
            authors = ", ".join(a.get("name", "") for a in r.get("authors", []))
            doi = ""
            for art in r.get("articleids", []):
                if art.get("idtype") == "doi":
                    doi = art.get("value", "")
                    break
            year = ""
            pubdate = r.get("pubdate", "")
            ym = re.match(r"(\d{4})", pubdate or "")
            if ym:
                year = ym.group(1)
            out.append(
                {
                    "id": f"pmid:{pid}",
                    "doi": doi,
                    "title": r.get("title", "").strip(),
                    "abstract": "",  # esummary doesn't return abstract; would need efetch
                    "year": year,
                    "authors": authors,
                    "journal": r.get("fulljournalname", "") or r.get("source", ""),
                    "source_db": "pubmed",
                    "source_query": technique["taxonomy_id"],
                }
            )
    return out


def search_openalex(technique: dict[str, Any], max_results: int = 200) -> list[dict[str, Any]]:
    terms = technique_terms(technique)
    primary = terms[0]
    # OpenAlex search supports phrase quoting
    query = f'"{primary}"'
    if len(terms) > 1:
        query += " OR " + " OR ".join(f'"{t}"' for t in terms[1:3])
    enc = urllib.parse.quote(query)
    url = (
        "https://api.openalex.org/works"
        f"?search={enc}"
        f"&per-page={min(max_results, 200)}"
        "&select=id,doi,title,abstract_inverted_index,publication_year,authorships,primary_location"
        f"&mailto=marzumm24@gmail.com"
    )
    body = http_get(url)
    data = json.loads(body.decode("utf-8"))
    out: list[dict[str, Any]] = []
    for w in data.get("results", [])[:max_results]:
        # Reconstruct abstract from inverted index
        abstract = ""
        inv = w.get("abstract_inverted_index")
        if inv:
            positions: dict[int, str] = {}
            for word, idxs in inv.items():
                for idx in idxs:
                    positions[idx] = word
            if positions:
                abstract = " ".join(positions[i] for i in sorted(positions.keys()))
        authors = ", ".join(
            a.get("author", {}).get("display_name", "")
            for a in (w.get("authorships") or [])
        )
        venue = ""
        ploc = w.get("primary_location") or {}
        src = ploc.get("source") or {}
        venue = src.get("display_name") or ""
        out.append(
            {
                "id": (w.get("id") or "").replace("https://openalex.org/", "openalex:"),
                "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                "title": (w.get("title") or "").strip(),
                "abstract": abstract,
                "year": str(w.get("publication_year") or ""),
                "authors": authors,
                "journal": venue,
                "source_db": "openalex",
                "source_query": technique["taxonomy_id"],
            }
        )
    return out


def search_semantic_scholar(technique: dict[str, Any], max_results: int = 100) -> list[dict[str, Any]]:
    terms = technique_terms(technique)
    primary = terms[0]
    enc = urllib.parse.quote(primary)
    url = (
        "https://api.semanticscholar.org/graph/v1/paper/search"
        f"?query={enc}"
        f"&limit={min(max_results, 100)}"
        "&fields=title,abstract,year,authors,externalIds,venue"
    )
    try:
        body = http_get(url)
    except RuntimeError as e:
        if "HTTP 429" in str(e):
            time.sleep(5)
            body = http_get(url)
        else:
            raise
    data = json.loads(body.decode("utf-8"))
    out: list[dict[str, Any]] = []
    for w in data.get("data", []):
        ext = w.get("externalIds") or {}
        doi = ext.get("DOI") or ""
        authors = ", ".join(a.get("name", "") for a in (w.get("authors") or []))
        out.append(
            {
                "id": f"s2:{w.get('paperId', '')}",
                "doi": doi,
                "title": (w.get("title") or "").strip(),
                "abstract": (w.get("abstract") or "").strip() or "",
                "year": str(w.get("year") or ""),
                "authors": authors,
                "journal": w.get("venue") or "",
                "source_db": "semantic_scholar",
                "source_query": technique["taxonomy_id"],
            }
        )
    return out


def search_crossref(technique: dict[str, Any], max_results: int = 100) -> list[dict[str, Any]]:
    terms = technique_terms(technique)
    primary = terms[0]
    enc = urllib.parse.quote(primary)
    url = (
        "https://api.crossref.org/works"
        f"?query={enc}"
        f"&rows={min(max_results, 100)}"
        "&select=DOI,title,abstract,published-print,published-online,author,container-title"
        f"&mailto=marzumm24@gmail.com"
    )
    body = http_get(url)
    data = json.loads(body.decode("utf-8"))
    out: list[dict[str, Any]] = []
    for w in data.get("message", {}).get("items", []):
        title = " ".join(w.get("title", []) or []).strip()
        abstract = (w.get("abstract") or "").strip()
        # Strip JATS XML tags from abstract
        abstract = re.sub(r"<[^>]+>", "", abstract)
        # Prefer print year
        year = ""
        for key in ("published-print", "published-online", "published"):
            d = w.get(key) or {}
            parts = d.get("date-parts") or [[]]
            if parts and parts[0]:
                year = str(parts[0][0])
                break
        authors = ", ".join(
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in (w.get("author") or [])
        )
        venue = " ".join(w.get("container-title", []) or []).strip()
        out.append(
            {
                "id": f"doi:{w.get('DOI', '')}",
                "doi": w.get("DOI", "") or "",
                "title": title,
                "abstract": abstract,
                "year": year,
                "authors": authors,
                "journal": venue,
                "source_db": "crossref",
                "source_query": technique["taxonomy_id"],
            }
        )
    return out


def search_arxiv(technique: dict[str, Any], max_results: int = 50) -> list[dict[str, Any]]:
    terms = technique_terms(technique)
    primary = terms[0]
    q = f'all:"{primary}" AND (cat:cs.CL OR cat:cs.AI OR cat:cs.HC OR cat:econ.GN)'
    enc = urllib.parse.quote(q)
    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query={enc}"
        f"&max_results={max_results}"
    )
    body = http_get(url, accept="application/atom+xml")
    text = body.decode("utf-8")
    out: list[dict[str, Any]] = []
    # Simple regex parse — Atom XML
    entries = re.findall(r"<entry>(.*?)</entry>", text, re.DOTALL)
    for e in entries:
        eid_m = re.search(r"<id>(.*?)</id>", e)
        title_m = re.search(r"<title>(.*?)</title>", e, re.DOTALL)
        summary_m = re.search(r"<summary>(.*?)</summary>", e, re.DOTALL)
        year_m = re.search(r"<published>(\d{4})", e)
        authors = re.findall(r"<name>(.*?)</name>", e)
        doi_m = re.search(r'<arxiv:doi[^>]*>([^<]+)</arxiv:doi>', e)
        arxiv_id = (eid_m.group(1).strip() if eid_m else "").replace("http://arxiv.org/abs/", "")
        out.append(
            {
                "id": f"arxiv:{arxiv_id}",
                "doi": (doi_m.group(1).strip() if doi_m else ""),
                "title": re.sub(r"\s+", " ", (title_m.group(1) if title_m else "").strip()),
                "abstract": re.sub(r"\s+", " ", (summary_m.group(1) if summary_m else "").strip()),
                "year": year_m.group(1) if year_m else "",
                "authors": ", ".join(authors),
                "journal": "arXiv",
                "source_db": "arxiv",
                "source_query": technique["taxonomy_id"],
            }
        )
    return out


def search_osf_registrations(technique: dict[str, Any], max_results: int = 50) -> list[dict[str, Any]]:
    terms = technique_terms(technique)
    primary = terms[0]
    enc = urllib.parse.quote(primary)
    url = (
        "https://api.osf.io/v2/registrations/"
        f"?filter[title][icontains]={enc}"
        f"&page[size]={min(max_results, 50)}"
    )
    try:
        body = http_get(url)
    except RuntimeError:
        return []
    data = json.loads(body.decode("utf-8"))
    out: list[dict[str, Any]] = []
    for r in data.get("data", []):
        attr = r.get("attributes", {})
        out.append(
            {
                "id": f"osf:{r.get('id', '')}",
                "doi": "",
                "title": (attr.get("title") or "").strip(),
                "abstract": (attr.get("description") or "").strip(),
                "year": (attr.get("date_registered") or "")[:4],
                "authors": "",
                "journal": "OSF Registrations",
                "source_db": "osf_registrations",
                "source_query": technique["taxonomy_id"],
            }
        )
    return out


def search_clinicaltrials(technique: dict[str, Any], max_results: int = 50) -> list[dict[str, Any]]:
    terms = technique_terms(technique)
    primary = terms[0]
    enc = urllib.parse.quote(primary)
    url = (
        "https://clinicaltrials.gov/api/v2/studies"
        f"?query.term={enc}"
        f"&pageSize={min(max_results, 100)}"
    )
    try:
        body = http_get(url)
    except RuntimeError:
        return []
    data = json.loads(body.decode("utf-8"))
    out: list[dict[str, Any]] = []
    for s in data.get("studies", []):
        proto = s.get("protocolSection") or {}
        ident = proto.get("identificationModule") or {}
        desc = proto.get("descriptionModule") or {}
        status = proto.get("statusModule") or {}
        out.append(
            {
                "id": f"nct:{ident.get('nctId', '')}",
                "doi": "",
                "title": (ident.get("officialTitle") or ident.get("briefTitle") or "").strip(),
                "abstract": (desc.get("briefSummary") or "").strip(),
                "year": (status.get("startDateStruct", {}).get("date") or "")[:4],
                "authors": "",
                "journal": "ClinicalTrials.gov",
                "source_db": "clinicaltrials",
                "source_query": technique["taxonomy_id"],
            }
        )
    return out


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

SEARCHERS = {
    "pubmed": (search_pubmed, 1.2),           # NCBI: 3/sec public, plus esummary
    "openalex": (search_openalex, 0.3),       # 10/sec polite-pool
    "semantic_scholar": (search_semantic_scholar, 6.0),  # ~100/5min unauthenticated
    "crossref": (search_crossref, 0.5),       # 50/sec polite-pool
    "arxiv": (search_arxiv, 3.0),             # 1 request per 3 seconds rule
    "osf_registrations": (search_osf_registrations, 0.7),
    "clinicaltrials": (search_clinicaltrials, 0.5),
}


def run(databases: list[str], max_per_query: int) -> dict[str, Any]:
    techniques = parse_taxonomy(TAXONOMY_PATH)
    print(f"[runner] Parsed {len(techniques)} techniques from taxonomy", flush=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    all_records: list[dict[str, Any]] = []
    log: dict[str, dict[str, int]] = {db: {} for db in databases}
    started = datetime.datetime.utcnow().isoformat() + "Z"
    for db in databases:
        if db not in SEARCHERS:
            print(f"[runner] Unknown database: {db}", file=sys.stderr)
            continue
        searcher, delay = SEARCHERS[db]
        db_dir = RAW_DIR / db
        db_dir.mkdir(parents=True, exist_ok=True)
        total = 0
        for t in techniques:
            tid = t["taxonomy_id"]
            try:
                rows = searcher(t, max_per_query)
            except Exception as e:
                print(f"  [{db}/{tid}] ERROR: {e}", flush=True)
                rows = []
                # back off on errors
                time.sleep(delay * 3)
            else:
                time.sleep(delay)
            log[db][tid] = len(rows)
            total += len(rows)
            (db_dir / f"{tid}.json").write_text(
                json.dumps(rows, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            all_records.extend(rows)
            print(f"  [{db}/{tid}] {len(rows)} hits", flush=True)
        print(f"[runner] {db}: {total} total hits", flush=True)
    finished = datetime.datetime.utcnow().isoformat() + "Z"
    # Write aggregated CSV
    fieldnames = [
        "id", "doi", "title", "abstract", "year",
        "authors", "journal", "source_db", "source_query",
    ]
    AGG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with AGG_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in all_records:
            w.writerow({k: r.get(k, "") for k in fieldnames})
    print(f"[runner] Wrote {len(all_records)} aggregated rows to {AGG_PATH}", flush=True)
    return {"started": started, "finished": finished, "log": log, "total": len(all_records)}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--databases", default=",".join(DEFAULT_DATABASES))
    p.add_argument("--max-per-query", type=int, default=100)
    args = p.parse_args()
    dbs = [d.strip() for d in args.databases.split(",") if d.strip()]
    summary = run(dbs, args.max_per_query)
    summary_path = REPO / "search" / "_run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[runner] Run summary saved to {summary_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
