# OSF Registries — Standard Pre-Registration

This file contains the pre-registered protocol of the Closing Evidence Atlas formatted to the [OSF Standard Pre-Registration template](https://osf.io/registries). The same content lives in `PROTOCOL.md` in academic narrative; this version is structured for direct paste into the OSF web form.

**Suggested registration title:** A pre-registered systematic review and Bayesian meta-analysis of empirically tested sales-closing techniques

**Suggested OSF subject(s):** Social and Behavioral Sciences · Psychology · Marketing

---

## 1. Study Information

### 1.1 Title

A pre-registered systematic review and Bayesian meta-analysis of empirically tested sales-closing techniques.

### 1.2 Authors

Marion Moranetz (sole author; affiliation: independent researcher).

### 1.3 Description

Sales-closing is a high-stakes commercial behavior with a century of practitioner-authored writing (Hopkins, Tracy, Voss, Sandler, Cialdini, Belfort, Dixon, Rackham). Across this corpus, hundreds of named "closing techniques" are described — assumptive, alternative-choice, summary, trial, takeaway, Ben Franklin, puppy-dog, sharp-angle, calibrated-question, and others — and taught with high confidence in commercial training programs.

The underlying empirical foundation has never been comprehensively audited. The few existing reviews (Schwepker 2003; Roman & Iacobucci 2010; Sherer 2013) are scoped to single sub-domains, pre-date modern meta-analytic standards (Borenstein et al. 2009), and pre-date the open-science reform movement (Simonsohn et al. 2014; Munafò et al. 2017).

This pre-registered review will:

1. Catalog every named sales-closing technique appearing in the practitioner literature (the **taxonomy step**).
2. Identify all empirical studies testing the effect of any cataloged technique on a closing-relevant outcome.
3. Extract effect sizes, study quality indicators, and contextual moderators.
4. Pool effects per technique using Bayesian random-effects meta-analysis with weakly-informative priors.
5. Audit publication bias (funnel plot asymmetry, Egger's test, p-curve, three-parameter selection model, PET-PEESE).
6. Run multiverse / specification-curve analyses over reasonable analytical decisions.
7. Report a final ranked list of closing techniques by **credibility-weighted effect size (CWES)**, with associated uncertainty intervals.

---

## 2. Hypotheses

**Primary RQ-1.** Among named sales-closing techniques described in the practitioner literature, which have credible empirical support — defined as at least one preregistered or independently replicated study with a standardized effect size whose 95% credible interval excludes zero in the practitioner-claimed direction?

**Primary RQ-2.** When effects are pooled via Bayesian random-effects meta-analysis with weakly-informative priors, what is the posterior distribution of the population effect for each technique? Which techniques have posterior medians and 95% credible intervals that survive a pre-registered multiverse-specification robustness check?

**Secondary RQ-3.** What contextual moderators (B2B vs. B2C; transactional vs. consultative; in-person vs. phone vs. digital; cultural region; immediate vs. delayed close) systematically modify technique efficacy?

**Secondary RQ-4.** What is the magnitude of publication-bias evidence in this literature?

**Secondary RQ-5.** What proportion of named techniques in the practitioner literature have *zero* empirical studies satisfying our inclusion criteria?

---

## 3. Sampling Plan

### 3.1 Data collection has begun

**Yes.** Stage-1 screening complete; Phase 2 extraction at 44 records as of 2026-05-11. This pre-registration is filed contemporaneously with the manuscript draft. The PROTOCOL.md file in the public repo carries a git commit hash dated before the corresponding Stage-1 screening decision was recorded; OSF reviewers can verify the timing chain via the public commit log.

### 3.2 Explanation of data collection schedule

Phase 1 (search + Stage-1 screening) completed 2026-05. Phase 2 (full-text extraction) is ongoing. Phase 3 (Bayesian meta-analysis + multiverse + bias diagnostics) follows once Phase 2 reaches the target N for the strongest-evidenced techniques (~30 records per technique).

### 3.3 Sample size

Final sample size is not pre-specified at a fixed number because this is a systematic review (not a primary study). The sample is **every peer-reviewed empirical study satisfying the inclusion criteria, recovered from the 7 pre-registered public databases.**

Stage-1 screening identified 572 included records from 11,785 unique records. Final Stage-2-passing N is expected to fall in the 115-230 range after attrition.

### 3.4 Sample size rationale

Per-technique meta-analyses require k ≥ 5 to be reported with Phase 3 pooled posteriors (pre-registered threshold). Techniques with k = 1-4 are reported descriptively. Techniques with k = 0 are reported as "empirical deserts" in the survivor table.

### 3.5 Stopping rule

No stopping rule. Every record matching the inclusion criteria is included.

---

## 4. Variables

### 4.1 Manipulated variables

Not applicable — this is a systematic review of existing experimental literature. The "manipulated variable" is the **closing technique** as deployed in the underlying primary studies.

### 4.2 Measured variables

Per included study, extracted variables (full schema in `search/extraction_form.md`):

- Bibliographic — DOI, authors, year, title, journal
- Study design — RCT / quasi-experimental / observational / field-experimental / lab
- Sample — n_total, n_per_arm, population, participant role
- Setting — sales context (B2B / B2C / charitable / health), channel (in-person / phone / web)
- Intervention — technique-taxonomy ID, operationalization verbatim, comparator type
- Outcome — outcome type, measurement method, effect size + metric + 95% CI + p-value
- Quality — pre-registration status, funding source, RoB rating (Cochrane RoB 2.0 / ROBINS-I)
- Provenance — extraction date, extractor identifier, source URL

### 4.3 Indices

Per technique, indices computed:

- Pooled posterior μ (median, 95% credible interval) under Bayesian random-effects model
- τ (between-study heterogeneity)
- P(μ > 0) and P(μ > 0.2) (practical-significance probability)
- Multiverse-specification robustness — proportion of 486 analytical specifications yielding 95% CrI excluding zero
- Publication-bias-adjusted estimate (PET-PEESE, three-parameter selection)

---

## 5. Design Plan

### 5.1 Study type

Systematic review with Bayesian random-effects meta-analysis. PRISMA 2020 conformant. Eligible for PROSPERO co-registration.

### 5.2 Blinding

Not applicable (review of existing studies).

### 5.3 Study design

Three-phase architecture (see `PROTOCOL.md` §3 for full detail):

- **Phase 1** — pre-registered systematic search of 7 public databases (PubMed, OpenAlex, Crossref, Semantic Scholar, arXiv, OSF Registrations, ClinicalTrials.gov). Stage-1 title-abstract screening combining heuristic exclusion + LLM-assisted individualized review.
- **Phase 2** — full-text extraction of effect sizes per the 34-column form. Risk-of-bias rating per Cochrane RoB 2.0 / ROBINS-I.
- **Phase 3** — per-technique Bayesian random-effects meta-analysis (`brms` + Stan, weakly-informative priors: μ ~ N(0, 0.5) on Hedges' *g* scale; τ ~ Half-Normal(0, 0.3)).
- **Phase 4** — multiverse-specification robustness across 486 reasonable analytical decisions (Steegen et al. 2016; Simonsohn et al. 2020) + publication-bias diagnostics + sensitivity analyses.

### 5.4 Randomization

Not applicable.

---

## 6. Analysis Plan

### 6.1 Statistical models

- Bayesian random-effects meta-analysis per technique using `brms` (Stan backend) with weakly-informative priors: μ ~ Normal(0, 0.5) on Hedges' *g*; τ ~ Half-Normal(0, 0.3).
- DerSimonian-Laird method-of-moments τ² estimator for the importance-sampling pilot (`scripts/pilot_meta_analysis.py`) — a pure-stdlib pilot for rapid iteration; the protocol-conformant analysis uses Stan-MCMC.
- Multiverse-specification analysis across 486 pre-registered analytical decisions per technique.
- Publication-bias diagnostics: funnel plot asymmetry · Egger's test · p-curve · three-parameter selection model · PET-PEESE adjustment.

### 6.2 Transformations

Effect sizes standardized to **Hedges' *g*** (continuous outcomes) or **log-odds-ratio** (binary outcomes) via `metafor::escalc` conversions. The pilot script implements approximate variants of these conversions for rapid iteration; the protocol-conformant Phase 3 run uses the canonical `escalc` implementations.

### 6.3 Inference criteria

A technique is classified as a **survivor** if ALL five of the following pre-registered criteria are met:

1. k ≥ 5 eligible studies
2. 95% credible interval on the pooled μ excludes zero
3. ≥ 80% of multiverse-specification analyses produce credible intervals excluding zero
4. Effect remains practically significant (μ > 0.2 on Cohen's *d* scale, or equivalent on log-OR) under PET-PEESE bias adjustment
5. Effect is not solely driven by industry-funded primary studies (sensitivity analysis stratified by funding source)

### 6.4 Data exclusion

Records excluded at Stage-1 if they fail any of the pre-registered inclusion criteria (`search/inclusion_criteria.md`). Records excluded at Stage-2 if full-text review reveals: non-experimental design, no extractable effect size, or operationalization that does not actually deploy the named technique.

### 6.5 Missing data

For records with retrievable abstract but no extractable effect size (e.g., institutional-repo abstract-only sources), the record is kept in the dataset with effect-size fields marked `not-reported`. These records contribute to the inclusion-count but are excluded from the meta-analytic pool.

### 6.6 Exploratory analysis

Pre-specified moderator analyses (per technique with sufficient k):

- B2B vs. B2C
- Lab vs. field
- Cultural region
- Channel (in-person / phone / web)
- Time-to-outcome (immediate vs. delayed)

Exploratory findings clearly labeled as such in the final report.

---

## 7. Other

### 7.1 Deviation log

All pre-registered deviations are transparently logged in `PROTOCOL_DEVIATIONS.md`. Each deviation includes the pre-registered original, the revision, and the empirical justification (recorded before the relevant data was inspected wherever possible).

As of 2026-05-11, the deviation log contains 6 entries (Deviations 001-006) covering: public-databases-only restriction (Deviation 001), screening-protocol refinements (002-004), low-priority deferred exclusion (Deviation 005), and effect-size-conversion parser extensions (006).

### 7.2 Materials

All materials are public and version-controlled at:

**https://github.com/Moranetz/closing-evidence-atlas**

Including:

- `PROTOCOL.md` — academic-narrative protocol (binding version)
- `PROTOCOL_DEVIATIONS.md` — deviation log
- `manuscript/atlas_v0.1.md` — preprint draft
- `manuscript/cro_summary.md` — CRO-readable summary (this companion file)
- `taxonomy/techniques.md` — 39-technique catalog with practitioner sources
- `search/strategy.md` — per-technique database query strings
- `search/inclusion_criteria.md` — Stage-1 inclusion rules
- `search/extraction_form.md` — 34-column extraction schema
- `data/extracted_studies_pilot.csv` — Phase 2 extraction dataset
- `scripts/pilot_meta_analysis.py` — pure-stdlib Bayesian importance-sampling pilot
- `scripts/sensitivity_analysis.py` — sensitivity-analysis battery
- `scripts/classify_oa_extractability.py` — OA-extractability classifier
- `analysis/01-05_*.R` — protocol-conformant R + brms scripts (full Phase 3)

### 7.3 Conflicts of interest

The author has no commercial relationship with any sales-training program, software vendor, or organization that would benefit from a specific finding direction. The author is preparing for an AE role in a commercial-sales context; this review is being conducted as part of a larger personal research program. This relationship is disclosed transparently and is unlikely to bias methodology choices given the strong pre-registration commitments.

### 7.4 Data sharing

Anonymized extraction dataset will be deposited to OSF under CC-BY-4.0 license at Phase 3 completion. The dataset deposit will include: per-record extracted variables, effect-size standardization decisions, RoB ratings, and the final Bayesian model fits.

---

## Reviewer notes (not part of the registration form)

This pre-registration is being filed contemporaneously with substantial work in progress:

- Stage-1 screening: complete
- Phase 2 extraction: 44 of expected 115-230 records
- Phase 3 pilot: importance-sampling variant complete; protocol-conformant Stan-MCMC pending R/brms install
- Calibration κ check: pending second-rater pass on `search/calibration_sample_blind.csv`

The pre-registration is therefore "Type 2" in the OSF taxonomy: pre-registered AFTER initial data collection but BEFORE the headline analysis (Phase 3 pooling + multiverse + bias adjustment). The PROTOCOL.md file in the public repo carries a git commit hash that pre-dates the Stage-1 screening decisions, providing a verifiable timing chain for reviewers.

---

*Filed under the Standard Pre-Registration template. OSF DOI will be added here upon registration.*
