#!/usr/bin/env python3
"""
High-precision heuristic first-pass exclusion for clearly-irrelevant records.

Rule (auto-exclude only if BOTH of the following hold):
  (A) Venue OR title strongly signals out-of-scope domain
      (chemistry, materials, dental, orthopedic, neuroscience, biochem,
       geoscience, petroleum, AI/ML, astronomy, mathematics, pure-clinical,
       archaeology, philology), AND
  (B) Abstract contains NO commercial/persuasion context terms from the
      allowlist (consumer, compliance, purchase, negotiation, marketing,
      donation, advertising, salesperson, buyer, ...).

The conjunction makes the rule conservative: borderline records (e.g., a
chemistry paper that happens to mention 'consumer' in the abstract) are NOT
auto-excluded; they flow to LLM screening.

Outputs decisions to `decision`, `decision_reason`, `screener=heuristic-v1`,
`decision_date` on the master `search/screening_stage1.csv`.

Stdlib only. Pre-registered as Deviation 004 in PROTOCOL_DEVIATIONS.md.
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

# Out-of-scope venue tokens (case-insensitive substring match against `journal`)
VENUE_BLOCKLIST = [
    # Hard sciences
    "materials science", "materials and", "polymers", "polymer",
    "chemistry", "chemical eng", "chemphyschem", "biochemistry",
    "organic letters", "inorganic", "analytical chem", "molecular",
    "molecular biology", "biophys", "molecular cell", "cell research",
    "biotechnology", "nanomaterials", "nanostructure", "crystallography",
    "geoscience", "petroleum", "geophysical", "tectonophysics",
    "geochemistry", "atmospheric", "environmental pollution",
    "astrophys", "astronomy",
    "physics", "applied physics", "physical review", "phys rev",
    "fluid mechanics", "engineering and", "engineering: a",
    "engineering structures", "structural engineering",
    "concrete", "construction", "civil eng", "civil engineering",
    "protective structures",
    "mathematics", "mathematical", "mathematik",
    "neuroscience", "neuroimage", "neural plasticity", "neurology",
    "neural network", "neural computation",
    # Pure clinical
    "orthodontic", "orthopaedic", "orthopedic", "dentistry", "dental",
    "cardiology", "oncology", "rheumatology", "psychiatry",
    "ophthalmology", "dermatology", "urology", "nephrology",
    "gastroenterology", "hepatology", "endocrinology", "pulmonology",
    "respiratory", "pneumology", "anaesthesia", "anesthesia",
    "transplantation", "intensive care", "critical care",
    "surgery", "surgical", "spine",
    "alcohol and alcoholism", "psychopharmacology",
    "pediatric", "paediatric",
    # CS / ML (unless adjacent to behavior)
    "computer science", "machine learning", "neural information",
    "knowledge discovery",
    # Other
    "agriculture", "agricultural", "veterinary", "fisheries",
    "archaeology", "archaeolog",
    "philology", "philosophical review", "classical philology",
    "literature", "literary",
    "music theory", "musicology",
    "geology", "mineral",
]

# Out-of-scope title tokens (require ≥ 2 matches to trigger)
TITLE_TOKENS = [
    # Chemistry / materials
    "synthesis", "characterization", "characterisation", "crystallograph",
    "diffraction", "spectroscopy", "spectrometry", "catalyst", "catalytic",
    "nanoparticle", "nanostruc", "polymer", "oligonucleotide",
    "thermodynamic", "kinetic", "polymeriza",
    # Bio
    "phylogen", "protein", "enzyme", "gene expression", "rna ",
    "dna ", "cell line", "cancer", "tumor", "tumour",
    "mouse model", "rat model", "in vivo", "in vitro",
    "amino acid", "receptor", "signaling pathway", "signalling pathway",
    "ligand", "histone", "transcription",
    "biochemical", "biomedical",
    # Physics
    "quantum", "tensor", "lattice", "electron",
    # CS / ML
    "neural architecture", "neural network", "gradient descent",
    "backpropagation", "convolutional", "transformer",
    "few-shot", "zero-shot", "fine-tun",
    "graph neural", "embedding space",
    # Pure clinical
    "atopic", "diabetes mellitus", "myocardial",
    "biopsy", "histology", "pathology",
    "lipid", "triglyceride", "cholesterol",
    # Geology
    "tectonics", "faults",
    # Misc obviously not commercial
    "phylogeny",
]

# Commercial/persuasion allowlist — presence in abstract overrides venue/title heuristics
ALLOWLIST = [
    # Sales context
    "consumer", "customer", "buyer", "salesperson", "sales rep",
    "shopper", "shopping", "retail", "marketing", "advertis",
    "negotiat", "purchas", "buying decision", "willingness to pay",
    "willingness to buy", "donat",
    "telesale", "outbound", "ecommerce", "e-commerce",
    # Compliance/influence
    "compliance", "comply", "obedien", "persuad", "persuas",
    "influence tactic", "social influence", "foot-in-the-door",
    "door-in-the-face", "low-ball", "lowball", "anchor",
    "framing", "social proof", "scarcity claim", "scarcit",
    "reciprocity", "authority cue", "request for compliance",
    # Behavioral outcomes
    "purchase intent", "buying intent", "intent to buy",
    "conversion rate", "compliance rate",
    "deal closed", "close rate", "win rate",
    # Domain markers
    "behavior chang", "behaviour chang", "intervention to",
    "field experiment", "randomi", "experimental manipulation",
]


def has_any(needle_list: list[str], hay: str) -> bool:
    hay_low = hay.lower()
    return any(n in hay_low for n in needle_list)


def count_matches(needle_list: list[str], hay: str) -> int:
    hay_low = hay.lower()
    return sum(1 for n in needle_list if n in hay_low)


def classify(row: dict[str, str]) -> tuple[str | None, str]:
    """Return (decision, reason) or (None, '') if heuristic abstains."""
    title = (row.get("title") or "")
    journal = (row.get("journal") or "")
    abstract = (row.get("abstract") or "")

    venue_hit = has_any(VENUE_BLOCKLIST, journal) or has_any(VENUE_BLOCKLIST, title)
    title_token_count = count_matches(TITLE_TOKENS, title)
    abstract_allow = has_any(ALLOWLIST, abstract) or has_any(ALLOWLIST, title)

    # Rule A: out-of-scope venue + no commercial signal in abstract → exclude
    if venue_hit and not abstract_allow:
        return ("exclude", "heuristic-v1: out-of-scope venue with no commercial-persuasion signal in abstract")

    # Rule B: ≥ 2 out-of-scope title tokens + no commercial signal → exclude
    if title_token_count >= 2 and not abstract_allow:
        return ("exclude", f"heuristic-v1: {title_token_count} out-of-scope title tokens with no commercial-persuasion signal in abstract")

    # Rule C: empty title and empty abstract → exclude (no information to screen)
    if not title.strip() and not abstract.strip():
        return ("exclude", "heuristic-v1: empty title and empty abstract")

    return (None, "")


def validate_against_calibration() -> dict:
    """Run classifier on the 100-record calibration set and compute precision
    against LLM ground truth."""
    with CALIB_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    auto_excluded = []
    disagreements = []
    for r in rows:
        d, reason = classify(r)
        if d == "exclude":
            auto_excluded.append(r)
            llm_dec = (r.get("decision") or "").strip()
            if llm_dec != "exclude":
                disagreements.append(
                    {
                        "id": r["id"],
                        "title": (r.get("title") or "")[:80],
                        "llm_decision": llm_dec,
                        "heuristic_reason": reason,
                    }
                )
    n_auto = len(auto_excluded)
    n_disagree = len(disagreements)
    precision = (n_auto - n_disagree) / n_auto if n_auto > 0 else float("nan")
    return {
        "auto_excluded": n_auto,
        "disagreements": n_disagree,
        "precision": precision,
        "disagreements_list": disagreements,
    }


def apply_to_master() -> dict:
    """Apply classifier to master screening CSV, skipping records already screened."""
    with SCREENING_PATH.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []
    today = datetime.date.today().isoformat()
    counts = Counter()
    for r in rows:
        if (r.get("decision") or "").strip():
            counts["skipped (already screened)"] += 1
            continue
        d, reason = classify(r)
        if d is None:
            counts["abstain → needs LLM"] += 1
            continue
        r["decision"] = d
        r["decision_reason"] = reason
        r["screener"] = "heuristic-v1"
        r["decision_date"] = today
        counts[d] += 1
    with SCREENING_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return dict(counts)


def main() -> int:
    print("=== HEURISTIC VALIDATION on calibration set ===")
    val = validate_against_calibration()
    print(f"Auto-excluded: {val['auto_excluded']}")
    print(f"Disagreements with LLM (false positives): {val['disagreements']}")
    print(f"Precision vs LLM: {val['precision']:.3f}")
    if val["disagreements_list"]:
        print("\nDisagreements:")
        for d in val["disagreements_list"]:
            print(f"  - {d['id']}: LLM={d['llm_decision']} — {d['title']}")
            print(f"    heuristic reason: {d['heuristic_reason']}")
    if val["precision"] < 0.98:
        print(f"\nFAIL: precision {val['precision']:.3f} < 0.98 threshold.")
        print("Refusing to apply to master CSV. Tighten rules and re-run.")
        return 2
    print("\nPASS — applying to master CSV.")
    counts = apply_to_master()
    print(f"\n=== APPLIED TO MASTER ===")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
