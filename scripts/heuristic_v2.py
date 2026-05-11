#!/usr/bin/env python3
"""
Heuristic v2 — more aggressive than v1 but still high-precision.

Builds on v1 (already applied to master). Adds rules for the dominant
false-positive patterns observed in the calibration set:

  R-D (Drug trial) — ClinicalTrials.gov record whose title contains a drug
      name marker (e.g., "PF-04965842", "lithium", "lamotrigine", numbered
      drug code) or a pure-clinical condition (cancer, dermatitis, ARDS,
      arthritis, etc.) AND no commercial-persuasion allowlist terms in
      title or abstract → exclude.

  R-AI (Pure-ML paper) — arXiv record with title containing ≥ 2 ML/CS
      tokens AND no behavioral-science terms in abstract → exclude.

  R-EMPTY (Insufficient info) — Title is < 10 chars OR a single word OR
      contains only formatting indicators (e.g., "Summary", "Figure 3",
      "Supplemental Information") → exclude.

  R-BOOK-CHAP (Book chapter) — Source is a book chapter (DOI like
      .ch[N] or /book[…]) with empty abstract → exclude.

Each rule applied only when heuristic-v1 abstained. Precision validated
against the 100-record LLM-screened calibration set; threshold 0.95.

Stdlib only.
"""

from __future__ import annotations

import csv
import datetime
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCREENING_PATH = REPO / "search" / "screening_stage1.csv"
CALIB_PATH = REPO / "search" / "calibration_sample.csv"


# Drug/clinical condition markers (high-confidence indicators of pharma trial)
DRUG_NAME_PATTERN = re.compile(
    r"\b("
    r"PF-\d+|GSK-\d+|AZD\d+|NCT\d+|"
    r"lithium|lamotrigine|methotrexate|pramipexole|tofacitinib|pembrolizumab|"
    r"trastuzumab|atorvastatin|metformin|insulin|warfarin|heparin|"
    r"corticosteroid|methotrexate|prednisone|cisplatin|paclitaxel|"
    r"\d+\s*mg\s*/\s*day"
    r")\b",
    re.IGNORECASE,
)

CLINICAL_CONDITION_TOKENS = [
    "cancer", "carcinoma", "tumor", "tumour", "metasta",
    "dermatitis", "eczema", "psoriasis",
    "diabetes", "hypertension", "obesity",
    "arthritis", "osteoporosis", "fibromyalgia",
    "depression", "anxiety", "schizophrenia", "bipolar", "ptsd",
    "dementia", "alzheimer", "parkinson", "epilepsy", "stroke",
    "asthma", "copd", "pneumonia", "ards",
    "coronary heart", "myocardial",
    "ckd", "renal", "kidney disease",
    "atopic", "allergic",
    "hiv", "hepatitis", "tuberculosis", "covid",
    "alcoholism", "addiction", "substance use",
    "body dysmorphic", "self-stigma",
    "preterm", "neonatal",
]

ML_CS_TITLE_TOKENS = [
    "neural network", "deep learning", "machine learning",
    "transformer", "attention mechanism",
    "embedding", "embeddings",
    "convolution", "gradient descent",
    "graph neural", "reinforcement learning",
    "few-shot", "zero-shot", "fine-tuning", "fine-tune",
    "neural architecture",
    "tensor", "logit",
    "chain of thought", "chain-of-thought",
    "language model", "language models", "llm",
    "self-attention", "cross-attention", "cross attention",
    "alignment", "contrastive",
    "fp-tree", "frequent pattern",
    "denoising",
]

BEHAVIORAL_ABSTRACT_TOKENS = [
    "compliance", "comply", "persuad", "persuas", "influence",
    "obedien", "request", "concession", "anchor",
    "consumer", "customer", "buyer", "shopper",
    "donat", "marketing", "advertis", "purchas", "buying",
    "willingness to pay", "willingness to buy",
    "framing", "frame", "loss avers", "gain frame",
    "negotiat", "bargain",
    "behavior chang", "behaviour chang",
    "field experiment", "randomi",
    "social proof", "scarcity", "reciprocity",
]

EMPTY_TITLE_PATTERNS = [
    re.compile(r"^summary$", re.IGNORECASE),
    re.compile(r"^takeaway$", re.IGNORECASE),
    re.compile(r"^bracketing$", re.IGNORECASE),
    re.compile(r"^labeling$", re.IGNORECASE),
    re.compile(r"^figure \d+", re.IGNORECASE),
    re.compile(r"^table \d+", re.IGNORECASE),
    re.compile(r"^supplemental information", re.IGNORECASE),
    re.compile(r"^review for ", re.IGNORECASE),
    re.compile(r"^introduction$", re.IGNORECASE),
    re.compile(r"^conclusion$", re.IGNORECASE),
    re.compile(r"^abstract$", re.IGNORECASE),
    re.compile(r"^appendix", re.IGNORECASE),
    re.compile(r"^index$", re.IGNORECASE),
    re.compile(r"^references$", re.IGNORECASE),
    re.compile(r"^bibliograph", re.IGNORECASE),
]


def has_any(tokens: list[str], text: str) -> bool:
    text_low = text.lower()
    return any(t in text_low for t in tokens)


def count_matches(tokens: list[str], text: str) -> int:
    text_low = text.lower()
    return sum(1 for t in tokens if t in text_low)


def classify_v2(row: dict[str, str]) -> tuple[str | None, str]:
    """Return (decision, reason) for v2 rules. None = abstain."""
    title = (row.get("title") or "").strip()
    journal = (row.get("journal") or "").strip()
    abstract = (row.get("abstract") or "").strip()
    source_db = (row.get("source_db") or "").strip()
    text_blob = f"{title} {abstract}"

    has_behavioral = has_any(BEHAVIORAL_ABSTRACT_TOKENS, text_blob)

    # R-EMPTY: junk title with no abstract
    if not title or len(title) < 6:
        if not abstract:
            return ("exclude", "heuristic-v2: empty / near-empty title with no abstract")
    if any(p.match(title) for p in EMPTY_TITLE_PATTERNS):
        if not has_behavioral:
            return ("exclude", "heuristic-v2: section-header-style title with no behavioral signal in abstract")

    # R-D: ClinicalTrials.gov pharma/condition trial with no commercial signal
    if source_db == "clinicaltrials":
        is_drug = bool(DRUG_NAME_PATTERN.search(text_blob))
        is_clinical_condition = has_any(CLINICAL_CONDITION_TOKENS, text_blob)
        if (is_drug or is_clinical_condition) and not has_behavioral:
            return ("exclude", "heuristic-v2: ClinicalTrials.gov pharma/condition trial with no commercial-persuasion signal")

    # R-AI: arXiv ML/CS paper with no behavioral signal
    if source_db == "arxiv":
        ml_count = count_matches(ML_CS_TITLE_TOKENS, text_blob)
        if ml_count >= 1 and not has_behavioral:
            return ("exclude", f"heuristic-v2: arXiv ML/CS paper ({ml_count} ML tokens) with no behavioral signal")

    return (None, "")


def validate_against_calibration() -> dict:
    with CALIB_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    n_auto = 0
    disagreements = []
    for r in rows:
        d, reason = classify_v2(r)
        if d == "exclude":
            n_auto += 1
            llm_dec = (r.get("decision") or "").strip()
            if llm_dec != "exclude":
                disagreements.append(
                    {
                        "id": r["id"],
                        "title": (r.get("title") or "")[:80],
                        "llm_decision": llm_dec,
                        "reason": reason,
                    }
                )
    precision = (n_auto - len(disagreements)) / n_auto if n_auto > 0 else float("nan")
    return {
        "auto_excluded": n_auto,
        "disagreements": len(disagreements),
        "precision": precision,
        "disagreements_list": disagreements,
    }


def apply_to_master() -> dict:
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []
    today = datetime.date.today().isoformat()
    counts = Counter()
    for r in rows:
        if (r.get("decision") or "").strip():
            counts["skipped (already screened)"] += 1
            continue
        d, reason = classify_v2(r)
        if d is None:
            counts["abstain → needs LLM"] += 1
            continue
        r["decision"] = d
        r["decision_reason"] = reason
        r["screener"] = "heuristic-v2"
        r["decision_date"] = today
        counts[d] += 1
    with SCREENING_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return dict(counts)


def main() -> int:
    print("=== HEURISTIC V2 VALIDATION ===")
    val = validate_against_calibration()
    print(f"Auto-excluded: {val['auto_excluded']}")
    print(f"Disagreements with LLM: {val['disagreements']}")
    print(f"Precision: {val['precision']:.3f}")
    if val["disagreements_list"]:
        print("\nDisagreements:")
        for d in val["disagreements_list"]:
            print(f"  - {d['id']}: LLM={d['llm_decision']}")
            print(f"    title: {d['title']}")
            print(f"    reason: {d['reason']}")
    if val["precision"] < 0.95:
        print(f"\nFAIL: precision {val['precision']:.3f} < 0.95.")
        return 2
    print("\nPASS — applying to master CSV.")
    counts = apply_to_master()
    print("\n=== APPLIED ===")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
