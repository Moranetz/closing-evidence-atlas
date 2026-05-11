# closing-evidence-atlas

> A pre-registered systematic review and Bayesian meta-analysis of sales-closing techniques. The empirical foundation of the **Closer Foundation** research program.

**Status:** Phase 1 (Stage-1 screening) complete. Phase 2 (full-text extraction) at 19 records — **gain-framing now at k=10 and loss-framing at k=8**, both above the k≥5 Phase 3 meta-analysis threshold. Phase 3 pilot complete on importance-sampled posteriors; production R/brms run pending Marion-action. This README will be revised with verified Bayesian effect-size receipts after Atlas-G2.

---

## The premise

Most sales-closing literature is folklore. Hopkins, Tracy, Voss, Sandler, Cialdini, Belfort, Dixon, Rackham, Adamson — across the practitioner canon, more than 200 named "closing techniques" are taught with high confidence in commercial training programs. The empirical foundation under those techniques has never been comprehensively audited.

This repo does the audit. Pre-registered protocol. Public databases. Bayesian random-effects meta-analysis. Multiverse-specification robustness. Honest reporting of what survives, what doesn't, and what was never tested in the first place.

The point is not to dismiss the practitioner literature. The point is to separate three different things that practitioner books collapse into one blur: **what is taught**, **what is empirically supported**, and **what actually moves behavior at a level meta-analytically distinguishable from noise**.

## What it actually does

The pipeline decomposes the audit into named primitives:

- **Taxonomy.** 39 named closing techniques cataloged from the practitioner literature, with practitioner-claimed mechanism, claimed direction, and high-level cluster (compliance, framing, structural-close, social-cue, question-form, negotiation-anchor, post-objection, closing-environment).
- **Search.** Pre-registered systematic search of 7 public databases (PubMed, OpenAlex, Crossref, Semantic Scholar, arXiv, OSF Registrations, ClinicalTrials.gov) plus targeted hand-search. PRISMA 2020-conformant.
- **Screening.** Stage-1 title-abstract screening combining (a) high-precision heuristic exclusion with calibration κ verification and (b) LLM-assisted individualized review against pre-registered inclusion criteria.
- **Extraction.** Structured per-study form: design, sample, intervention operationalization, comparator, outcome, effect size (standardized to Hedges' *g* or log-OR), risk-of-bias (Cochrane RoB 2.0 / ROBINS-I).
- **Meta-analysis.** Bayesian random-effects per technique (`brms` + Stan, weakly-informative priors). Publication-bias diagnostics (funnel plot, Egger's test, p-curve, three-parameter selection, PET-PEESE). Multiverse-specification robustness across 486 reasonable analytical decisions per technique.
- **Survivor classification.** Five pre-registered criteria: ≥5 eligible studies, 95% CrI excluding zero, ≥80% multiverse-specifications excluding zero, practical-significance under PET-PEESE adjustment, independence from commercial-interest funding.

## Phase 3 pilot — first Bayesian posterior estimates (very preliminary)

A pure-stdlib pilot of the random-effects Bayesian pipeline (`scripts/pilot_meta_analysis.py`) ran on the original 9-record Phase 2 extraction. With approximate η² → d and F → d conversions and `k=2` per technique, the posteriors are wide but real:

| Technique | k | μ median | 95% CrI | P(μ > 0) | P(μ > 0.2) |
| --- | ---: | ---: | --- | ---: | ---: |
| `extreme-anchor` | 2 | 0.439 | [0.043, 0.723] | 0.98 | 0.92 |
| `gain-framing` | 2 | 0.539 | [−0.200, 1.053] | 0.93 | 0.84 |

**Phase 2 has since scaled to 19 records via the MDPI + APA-OA expansion.** Per-technique k counts are now: gain-framing 10, loss-framing 8, extreme-anchor 3, concrete-construal 3, social-proof 3. The next-iteration Phase 3 pilot will rerun with the expanded data; both framing techniques now have enough records to support per-technique posteriors that can be reported alongside the Stage-1 finding without the k=2 caveat.

These are pilot-stage demonstrations of the full pipeline running end-to-end on real extracted data. The R/brms scripts in `analysis/` produce protocol-conformant Stan-MCMC inference when R + brms + cmdstanr is installed and Phase 2 has scaled to 30-100 records per technique.

## The current empirical landscape (Stage-1)

11,785 unique records identified across 7 public databases. 8,839 explicitly classified at Stage-1 screening. **572 included** for Stage-2 full-text screening.

Of 39 named techniques in the practitioner taxonomy:

- **14 techniques (36%)** have ≥ 5 Stage-1 included studies — eligible for Bayesian meta-analysis at Phase 3.
- **10 techniques (26%)** have 1–4 studies — too few for meta-analysis; reported descriptively.
- **15 techniques (38%)** have **zero** peer-reviewed empirical studies — the empirical deserts.

The deserts are named techniques taught with confidence in sales-training programs and books. They are: **assumptive close, alternative-choice close, summary close, trial close, takeaway close, Ben Franklin close, sharp-angle close, puppy-dog close, mutual close plan, multi-threading, isolate-the-objection, reverse-objection, accusation audit, SPIN implication question, SPIN need-payoff question, mirroring (verbal repetition), bracketing.**

This is not a claim that these techniques are ineffective. It is a claim that they have not been tested at the level of the pre-registered inclusion criteria — peer-reviewed randomized or quasi-experimental design with a behavioral outcome.

## Why it's interesting

Three findings the Stage-1 corpus already supports, pending Stage-2 + Stage-3 confirmation:

1. **The empirical foundation of sales-closing literature is concentrated.** Four techniques — gain framing, loss framing, foot-in-the-door, and door-in-the-face — account for **74% of the 572 Stage-1 included studies**. The literature is not evenly distributed across the named techniques the practitioner canon describes.

2. **A substantial fraction of named techniques are empirically untested in peer-reviewed public-database literature.** The DESERT list above is direct evidence for RQ-5 in the pre-registered protocol.

3. **The dominant techniques in the academic literature are not the ones most prominent in modern sales-training programs.** Sales-training programs lead with the structural closes (assumptive, alternative-choice, summary, trial, takeaway, puppy-dog). The academic literature concentrates on the compliance and framing techniques (FITD, DITF, gain/loss framing, lowball, regulatory fit). The two literatures barely overlap.

Whether the dominant academic techniques produce real, replicable effects after multiverse-specification and publication-bias adjustment is the Phase-3 question.

## At a glance

- Total unique records: **11,785** across 7 public databases (PubMed · OpenAlex · Crossref · Semantic Scholar · arXiv · OSF Registrations · ClinicalTrials.gov)
- Records with DOI: **8,969** (76%)
- Records with abstract: **7,074** (60%)
- Heuristic-excluded with 100% precision against calibration LLM: **1,228**
- Low-priority deferred (Deviation 005, priority_score < 0.10): **6,710**
- LLM-screened with individualized per-record reasons: **901**
- **Stage-1 included for full-text screening: 572**
- Stage-1 included earliest study: **1966 (Freedman & Fraser, JPSP — the original foot-in-the-door experiment)**
- Stage-1 included spans 7 decades and 60+ peer-reviewed venues
- Pre-registered deviations transparently logged: **6** (PROTOCOL_DEVIATIONS.md)

## The best entry points

If you are new to the repo:

- [PROTOCOL.md](PROTOCOL.md) — the pre-registered systematic-review protocol. Methodologically binding before any data was touched.
- [PROTOCOL_DEVIATIONS.md](PROTOCOL_DEVIATIONS.md) — every change to the protocol after Atlas-G0 sign-off, with empirical justification.
- [taxonomy/techniques.md](taxonomy/techniques.md) — the 39-technique cataloged taxonomy.
- [results/stage1_survivor_report.md](results/stage1_survivor_report.md) — the per-technique Stage-1 evidence-base summary. **Read this first to understand the headline finding.**
- [analysis/statistical_plan.md](analysis/statistical_plan.md) — Bayesian random-effects model specification + multiverse design (Phase 3).
- [search/strategy.md](search/strategy.md), [search/inclusion_criteria.md](search/inclusion_criteria.md), [search/extraction_form.md](search/extraction_form.md) — the binding methodological scaffold.
- [PLAN.md](PLAN.md) — the project ultraplan with phase breakdown.

## How the pipeline is organized

```
scripts/
  search_runner.py        — public-database search execution
  reaggregate.py          — rebuild aggregated CSV from raw JSON
  deduplicate.py          — by DOI then fuzzy title-author match
  heuristic_first_pass.py — high-precision domain-mismatch exclusion (100% κ-validated precision)
  heuristic_v2.py         — drug-trial / ML-paper / empty-title exclusion (100% precision)
  priority_score.py       — venue tier + allowlist density + methodology signal
  sample_calibration_set.py — stratified-random 100-record sample for inter-rater κ
  apply_screening_decisions.py — apply calibration-set decisions to master
  apply_priority_batch_decisions.py — apply per-batch LLM decisions
  apply_deviation_005.py  — low-priority-deferred exclusion at priority_score < 0.10
  stage1_technique_summary.py — per-technique include/exclude tabulation + survivor classification
  build_search_log.py     — auto-generate search_log.md
  prepare_screening.py    — produce screening CSV skeleton
  make_blind_calibration.py — blinded calibration sample for Marion's independent screen
  compute_kappa.py        — Cohen's κ between LLM and human screens
  sample_preview.py       — random sample of records for quality inspection
```

## What this is not

- Not a sales-training manual. It does not teach how to close.
- Not a productivity tool. It does not score or optimize live conversations.
- Not a closing-script generator. The empirical foundation gives no warrant for prescriptive advice; the practitioner books are the right source for that.
- Not a substitute for practice. Knowing which techniques have empirical support is upstream of becoming better at deploying them — and the literature on training-transfer says reading does not transfer to skill.

## Honest limitations

- **Public-databases-only restriction** (Deviation 001). Scopus, Web of Science, PsycInfo, ABI/INFORM, EBSCO Business Source Complete, and full-text ProQuest Dissertations were not searched. Coverage gap estimated at 5–15% of historical (pre-2000) marketing-journal records and a similar fraction of grey literature. OpenAlex + Semantic Scholar overlap heavily with Scopus/WoS via DOI resolution, so the gap is likely smaller in practice. Reported transparently in the final preprint.
- **Low-priority deferred exclusion** (Deviation 005). 6,710 records with priority_score < 0.10 were excluded heuristically without individual LLM review. Empirical justification: the LLM-screened include rate drops below 30% at priority_score < 0.42, with extrapolated < 5% for the < 0.10 tier. Sensitivity analysis tests alternative thresholds (0.05, 0.15) in the final preprint.
- **English-only.** Non-English-language studies were excluded per protocol § 4.7.
- **Solo-author screening at scale.** Per Deviation 003, the LLM-assisted re-screen is additive to single-human-screener-equivalent decisions. A 100-record calibration set is available for inter-rater κ verification at any time (`scripts/compute_kappa.py`).
- **Stage-1 evidence base ≠ Stage-3 survivor list.** A technique with 100 Stage-1 includes may have 20 Stage-2 includes and 0 Stage-3 survivors after Bayesian multiverse + publication-bias adjustment. The Stage-1 count is the eligibility threshold for analysis, not the analysis itself.

## Running it

```bash
# Install dependencies (Python ≥ 3.10 for ConvoKit; stdlib for the rest)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # added at Phase 2

# Reproduce the search (idempotent, ~30 minutes)
python3 scripts/search_runner.py

# Reproduce the aggregation + dedup
python3 scripts/reaggregate.py
python3 scripts/deduplicate.py

# Reproduce the screening pipeline
python3 scripts/heuristic_first_pass.py
python3 scripts/heuristic_v2.py
python3 scripts/priority_score.py
python3 scripts/apply_deviation_005.py

# Reproduce the Stage-1 survivor report
python3 scripts/stage1_technique_summary.py
```

LLM-screening decisions are recorded in `search/_priority_batch_*_decisions.json` and are reproducible from the JSON files; the LLM call is one-shot per record with full per-record reason logging.

## Series

This repo is part of the **Closer Foundation** research program. Sister repos (planned):
- `close-detector` — transformer classifier for closing-technique deployment in transcripts.
- `closer-sparring` — local-first practice agent calibrated against the Atlas survivors.
- `delta-mechanics` — Tan et al. (2016) replication of the Cornell ChangeMyView Winning Arguments paper (methodology credential).

## License

Code: MIT. Protocol, taxonomy, and extracted data: CC-BY-4.0.
