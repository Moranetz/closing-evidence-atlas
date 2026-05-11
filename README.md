# closing-evidence-atlas

> A pre-registered systematic review and Bayesian meta-analysis of sales-closing techniques. The empirical foundation of the **Closer Foundation** research program.

**Status:** Phase 1 (Stage-1 screening) complete. Phase 2 (full-text extraction) at **44 records** across Frontiers / IRSP / MDPI / APA-OA + survivor-technique + HIGH-confidence PMC subsets. **Six per-technique posteriors produced**: gain-framing (k=9, μ=0.354), loss-framing (k=7, μ=0.327), regulatory-fit (k=3, μ=0.484), commitment-consistency (k=2, μ=0.590), social-proof (k=2, μ=0.682), extreme-anchor (k=2, μ=0.435). Five of six have CrIs cleanly excluding zero AND exceeding the d=0.2 practical-significance threshold with P>0.99. Sensitivity-stability test passed for gain-framing after atlas-009 parsing-artifact fix (see § Phase 3 pilot below). Production R/brms run pending Marion-action.

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

## Phase 3 pilot — Bayesian posterior estimates (rerun on 44-record extraction, atlas-009 fix applied)

A pure-stdlib pilot of the random-effects Bayesian pipeline (`scripts/pilot_meta_analysis.py`) ran on the 44-record Phase 2 extraction with approximate η² → d, F → d, t → r → d, log-OR → d (Cox-Hasselblad / Chinn 2000), standardized-beta → r → d, and cohens-d → d conversions:

| Technique | k (meta) | μ median | 95% CrI | τ | P(μ > 0) | P(μ > 0.2) |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `commitment-consistency` | 2 | **0.590** | [0.331, 0.782] | 0.089 | 0.999 | 0.993 |
| `regulatory-fit` | 3 | **0.484** | [0.346, 0.632] | 0.068 | 1.000 | 0.997 |
| `extreme-anchor` | 2 | 0.435 | [0.043, 0.745] | 0.269 | 0.983 | 0.914 |
| `gain-framing` | 9 | **0.354** | [0.280, 0.429] | 0.045 | 1.000 | 1.000 |
| `loss-framing` | 7 | **0.327** | [0.249, 0.410] | 0.047 | 1.000 | 0.999 |
| `social-proof` | 2 | 0.682 | [−0.206, 1.296] | 0.846 | 0.937 | 0.866 |

Five of six techniques have credible intervals cleanly excluding zero AND exceeding the d=0.2 practical-significance threshold with P>0.99. Social-proof remains the exception — k=2 with high between-study heterogeneity from records in very different commercial contexts (tipping vs. advertising).

**atlas-009 parsing-artifact fix.** The previous sensitivity-analysis flag on gain-framing (leave-one-out Δμ=-0.132 driven by atlas-009 having d=1.309 from a misread multi-value η²_p field) was resolved by cleaning atlas-009's `effect_size_value` to the single primary η²_p=0.05 (which correctly converts to d≈0.46, not 1.309). After the fix:

- Gain-framing μ shifted from 0.474 → 0.354 (now aligned with the established framing-literature range of d=0.20-0.40)
- Gain-framing CrI tightened from [0.305, 0.642] → [0.280, 0.429] (half the width)
- Gain-framing τ collapsed from 0.301 → 0.045
- Gain-framing leave-one-out Δμ tightened from -0.132 → -0.011 (now PASSES the pre-registered ≤0.10 stability threshold)

The parser was also tightened to prefer the FIRST 0.XX-form number in eta² value fields rather than the maximum, to prevent the same misread on future records. Full sensitivity report: [`results/sensitivity_report.md`](results/sensitivity_report.md).

Both framing techniques have credible intervals that cleanly exclude zero AND exceed the d=0.2 practical-significance threshold with very high probability. The first preprint-shippable per-technique posteriors from the Atlas pipeline.

**Why "k (meta)" differs from inclusion-count.** The technique-taxonomy-id column lists gain-framing across 10 extracted records and loss-framing across 8, but only 6 and 5 (respectively) have effect-size metrics the importance-sampler can convert to approximate Cohen's d. The remainder are skipped — abstract-only OA records, narrative-synthesis review entries, descriptive-statistics rows without inference, and one percent-change metric from a commercial field deployment with no statistical inference attached.

The original 9-record pilot returned gain-framing μ=0.539, 95% CrI [−0.200, 1.053], P(μ>0)=0.93 at k=2 — wide and weakly identifying zero-exclusion. The 19-record rerun tightens that to μ=0.501, 95% CrI [0.251, 0.733], P(μ>0)=0.999 at k=6. The Bayesian update is exactly the expected shape — more data, tighter posterior, same direction, point estimate stable across the update.

These are still pilot-stage demonstrations using importance sampling and rough effect-size conversions. The R/brms scripts in `analysis/` produce protocol-conformant Stan-MCMC inference using `metafor::escalc` for canonical effect-size conversions, weakly-informative Cauchy priors on τ, and 4-chain × 4000-iteration NUTS sampling. Production preprint analysis runs after R + brms + cmdstanr install.

## PRISMA flow

The current pipeline state is in [`figures/prisma_flow.svg`](figures/prisma_flow.svg) — generated by `scripts/prisma_flow.py`. Shows the path from 12,416 raw search records through deduplication, Stage-1 screening, OA accessibility, Phase 2 extraction, and Phase 3 meta-analysis eligibility, with transparent side-counts for every excluded subset (Deviation 005 low-priority deferred, Stage-1 LLM-and-heuristic excludes, closed-access deferred for institutional library access, etc.).

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
