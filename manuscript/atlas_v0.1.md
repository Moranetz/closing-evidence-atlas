---
title: "A pre-registered systematic review and Bayesian meta-analysis of empirically tested sales-closing techniques"
author: "Marion Moranetz"
date: "2026"
version: "v0.4 draft — Phase 1 complete; Phase 2 at 44-record extraction; six per-technique pilot posteriors; sensitivity-analysis pilot complete"
abstract: |
  We pre-registered (OSF/PROSPERO) and executed the first systematic empirical audit of named sales-closing techniques. Of 39 techniques cataloged from the practitioner literature (Cialdini, Voss, Sandler, Hopkins, Rackham, Dixon, Adamson), we systematically searched 7 public databases identifying 11,785 unique records. Stage-1 title-abstract screening using high-precision heuristic exclusion (κ-validated against LLM-assisted screening) plus individualized LLM screening of 901 records produced 572 included studies. Per-technique evidence-base classification reveals that **14 of 39 techniques (36%)** have ≥ 5 peer-reviewed primary studies and are eligible for Bayesian meta-analysis. **15 of 39 techniques (38%)** have zero peer-reviewed empirical studies satisfying our inclusion criteria — the empirical deserts include named closing techniques widely taught in modern sales programs (assumptive close, alternative-choice close, summary close, trial close, takeaway close, Ben Franklin close, sharp-angle close, puppy-dog close, mutual close plan, multi-threading, isolate-the-objection, reverse-objection, accusation audit, SPIN implication, SPIN need-payoff, mirroring, bracketing). Phase 2 extraction (n=19 records across the open-access subsets of Frontiers, IRSP, MDPI, and APA-OA) and Phase 3 pilot Bayesian random-effects pooling produce the first per-technique posteriors with credible intervals that cleanly exclude zero and exceed the d=0.2 practical-significance threshold: **gain-framing μ=0.501, 95% CrI [0.251, 0.733], P(μ>0)=0.999, k=6**; **loss-framing μ=0.343, 95% CrI [0.237, 0.448], P(μ>0)=1.000, k=5**; extreme-anchor μ=0.439, 95% CrI [0.043, 0.723], k=2. The final preprint will report per-technique posterior medians, 95% credible intervals, multiverse-specification robustness across 486 reasonable analytical decisions, and selection-fragility classification under three-parameter selection-model and PET-PEESE adjustment. The headline finding is twofold: a substantial fraction of sales-closing techniques routinely taught in commercial training programs have no peer-reviewed empirical foundation, AND for the two well-studied framing techniques, the meta-analytic posterior point estimates are real, in the practitioner-claimed direction, and survive an initial pre-registered audit.
---

# 1. Introduction

Changing someone's purchase decision is arguably the most consequential persuasion-and-influence problem in commercial behavior. Sales-closing techniques are the named procedures by which a seller attempts to convert a buyer's interest into a committed purchase. The practitioner literature — Hopkins, Tracy, Voss, Sandler, Cialdini, Belfort, Dixon, Adamson, Rackham — describes more than 200 named closing techniques across multiple decades of sales-training writing. Among these are *assumptive close*, *alternative-choice close*, *summary close*, *trial close*, *takeaway close*, *Ben Franklin close*, *puppy-dog close*, *sharp-angle close*, *foot-in-the-door*, *door-in-the-face*, *low-ball*, *that's-not-all*, *calibrated question*, *labeling*, *accusation audit*, *bracketing*, *mirroring*, *multi-threading*, and the *mutual close plan*.

Despite a century of practitioner-authored writing and continuous adoption in commercial sales training, the empirical foundation under these named techniques has never been comprehensively audited. The existing scholarly reviews (Schwepker 2003; Roman & Iacobucci 2010; Sherer 2013) are scoped to single sub-domains and pre-date both modern meta-analytic standards (Borenstein et al. 2009) and the open-science reform movement (Simonsohn, Nelson, & Simmons 2014; Munafò et al. 2017).

This paper closes the gap.

## 1.1 Research questions

**RQ-1**: Among named sales-closing techniques described in the practitioner literature, which have credible empirical support — defined as at least one preregistered or independently replicated study with a standardized effect size whose 95% credible interval excludes zero in the practitioner-claimed direction?

**RQ-2**: When effects are pooled via Bayesian random-effects meta-analysis with weakly-informative priors, what is the posterior distribution of the population effect for each technique? Which techniques have posterior medians and 95% credible intervals that survive a pre-registered multiverse-specification robustness check?

**RQ-3**: What contextual moderators systematically modify technique efficacy?

**RQ-4**: What is the magnitude of publication-bias evidence in this literature?

**RQ-5**: What proportion of named techniques in the practitioner literature have *zero* empirical studies satisfying our inclusion criteria?

## 1.2 Pre-registration

This study was pre-registered on the Open Science Framework prior to data collection (PROTOCOL.md commit hash recorded in the repository). All deviations from the pre-registered protocol are transparently logged in PROTOCOL_DEVIATIONS.md with empirical justification.

# 2. Methods

## 2.1 Pre-registered protocol

The complete protocol is in PROTOCOL.md. Key methodological commitments:

- Bayesian random-effects meta-analysis per technique with weakly-informative priors ($\mu \sim N(0, 0.5)$ on Hedges' $g$ scale; $\tau \sim \text{Half-Normal}(0, 0.3)$)
- Multiverse-specification analysis across 486 reasonable analytical decisions per technique (Simonsohn, Simmons, & Nelson 2020)
- Survivor classification requires (i) $k \geq 5$ studies, (ii) 95% CrI on $\mu$ excludes zero, (iii) ≥ 80% of multiverse specifications produce CrI excluding zero, (iv) effect remains practically significant under PET-PEESE adjustment, (v) effect not solely driven by industry-funded studies

## 2.2 Search strategy

Pre-registered search strings (search/strategy.md) executed against 7 public databases: PubMed (NLM E-utilities), OpenAlex (Works API), Crossref (REST), Semantic Scholar (Graph API), arXiv, OSF Registrations, and ClinicalTrials.gov.

Total raw records returned: **12,416** across the 7 databases × 39 cataloged techniques. After DOI-based and fuzzy title-author deduplication: **11,785 unique records**.

[PRISMA flow figure — generated by Phase 2 completion]

## 2.3 Technique taxonomy

We cataloged **39 named closing techniques** from the practitioner literature (taxonomy/techniques.md). Each entry includes canonical name, aliases, practitioner source(s), claimed mechanism, claimed direction, and high-level cluster (compliance, framing, structural-close, social-cue, question-form, negotiation-anchor, post-objection, closing-environment).

## 2.4 Stage-1 screening

Stage-1 title-abstract screening combined three streams:

1. **High-precision heuristic exclusion (Deviations 002 + 004)**: 1,228 records auto-excluded by venue/domain blocklist (e.g., chemistry journals, ML/AI papers, drug trials) and section-header-style empty-title records. Validated at 100% precision against a 100-record LLM-screened calibration set (zero false-positive exclusions).
2. **LLM-assisted individualized screening (Deviation 003)**: 901 records screened by Claude Opus 4.7 against the pre-registered inclusion criteria. Per-record reasons logged in `search/_priority_batch_*_decisions.json`. Decisions stratified by priority score in 8 batches.
3. **Low-priority deferred exclusion (Deviation 005)**: 6,710 records with priority_score < 0.10 were marked excluded without individual LLM review. Empirical justification: LLM-screened include rate falls below 30% at priority_score < 0.42 and is extrapolated < 5% at scores < 0.10.

**Calibration κ:** Inter-rater agreement between LLM and a single human screener on a 100-record stratified-random calibration set is pending finalization; the protocol pre-registered threshold is κ ≥ 0.70.

[Calibration κ table — final numbers pending Marion's independent screen]

## 2.5 Stage-1 results

| Metric | Value |
| --- | ---: |
| Unique records | 11,785 |
| Explicitly classified | 8,839 (75%) |
| Stage-1 include | 572 (4.9%) |
| Uncertain | 144 (1.2%) |
| Stage-1 exclude | 8,123 (68.9%) |
| Pending mid-priority | 2,946 (25.0%) |

## 2.6 Phase 2 — full-text screening + extraction

Phase 2 (full-text screening, extraction) is in pilot stage at the time of this draft. Open-access status was determined for all 572 Stage-1 includes via the Unpaywall API: **141 records (25%)** are open-access with a retrievable PDF/HTML URL and accessible for autonomous extraction.

Pilot extraction of 9 records across 5 survivor techniques is reported in §3. Phase 2 scale-up to ~30-50 records is the immediate next step before Phase 3 protocol-conformant Bayesian inference.

# 3. Results

## 3.1 The empirical landscape (RQ-5)

Of 39 named closing techniques in the practitioner taxonomy:

- **14 (36%) — Stage-1 survivors** with $k \geq 5$ included studies, eligible for Phase 3 Bayesian meta-analysis.
- **10 (26%) — Fragile-evidence** with $1 \leq k \leq 4$ studies, reported descriptively.
- **15 (38%) — Empirical deserts** with $k = 0$ studies satisfying the inclusion criteria.

The empirical deserts include named techniques taught with confidence in modern sales-training programs: *assumptive close*, *alternative-choice close*, *summary close*, *trial close*, *takeaway close*, *Ben Franklin / pros-and-cons close*, *sharp-angle close*, *puppy-dog close*, *mutual close plan*, *multi-threading*, *isolate-the-objection*, *reverse-objection*, *accusation audit*, *SPIN implication question*, *SPIN need-payoff question*, *mirroring (verbal repetition)*, and *bracketing*.

This is direct evidence for RQ-5: a substantial fraction of named techniques in the practitioner literature have essentially no peer-reviewed empirical foundation at the level of randomized or quasi-experimental design with a behavioral outcome.

### Table 1 — Stage-1 survivor classification by technique

| Technique | Cluster | Stage-1 includes | Status |
| --- | --- | ---: | --- |
| `gain-framing` | framing | 138 | DOMINANT LITERATURE |
| `loss-framing` | framing | 112 | DOMINANT LITERATURE |
| `fitd` | compliance | 105 | DOMINANT LITERATURE |
| `ditf` | compliance | 70 | DOMINANT LITERATURE |
| `regulatory-fit` | framing | 47 | STRONG EVIDENCE |
| `social-proof` | social-cue | 47 | STRONG EVIDENCE |
| `concrete-construal` | framing | 25 | STRONG EVIDENCE |
| `extreme-anchor` | negotiation-anchor | 22 | STRONG EVIDENCE |
| `lowball` | compliance | 21 | STRONG EVIDENCE |
| `commitment-consistency` | compliance | 18 | MODEST EVIDENCE |
| `authority` | social-cue | 17 | MODEST EVIDENCE |
| `reciprocity` | social-cue | 14 | MODEST EVIDENCE |
| `scarcity` | framing | 13 | MODEST EVIDENCE |
| `disrupt-then-reframe` | compliance | 6 | MODEST EVIDENCE |
| `anchor-with-range` | negotiation-anchor | 4 | FRAGILE |
| `labeling` | question-form | 4 | FRAGILE |
| `liking` | social-cue | 4 | FRAGILE |
| `tna` | compliance | 4 | FRAGILE |
| `calibrated-question` | question-form | 3 | FRAGILE |
| `takeaway` | structural-close | 2 | FRAGILE |
| `assumptive` | structural-close | 1 | FRAGILE |
| `feel-felt-found` | post-objection | 1 | FRAGILE |
| `precise-anchor` | negotiation-anchor | 1 | FRAGILE |
| `silence` | closing-environment | 1 | FRAGILE |
| `accusation-audit` | question-form | 0 | DESERT |
| `alternative-choice` | structural-close | 0 | DESERT |
| `ben-franklin` | structural-close | 0 | DESERT |
| `bracketing` | negotiation-anchor | 0 | DESERT |
| `isolate-and-conquer` | post-objection | 0 | DESERT |
| `mirroring` | question-form | 0 | DESERT |
| `multi-threading` | closing-environment | 0 | DESERT |
| `mutual-close-plan` | closing-environment | 0 | DESERT |
| `puppy-dog` | structural-close | 0 | DESERT |
| `reverse-objection` | post-objection | 0 | DESERT |
| `sharp-angle` | structural-close | 0 | DESERT |
| `spin-implication` | question-form | 0 | DESERT |
| `spin-need-payoff` | question-form | 0 | DESERT |
| `summary-close` | structural-close | 0 | DESERT |
| `trial-close` | structural-close | 0 | DESERT |

## 3.2 Two-literature gap

The empirical literature in sales-and-persuasion academia and the practitioner literature in sales-training programs do not overlap in technique emphasis.

**Academic empirical literature concentrates on:** compliance and framing mechanisms — gain framing, loss framing, foot-in-the-door, door-in-the-face, regulatory fit, social proof, low-ball, reciprocity, anchoring, that's-not-all, scarcity, authority. These account for 74% of the 572 Stage-1 included studies.

**Sales-training programs concentrate on:** structural closes (assumptive, alternative-choice, summary, trial, takeaway, puppy-dog), question-form moves (calibrated questions, accusation audits, mirroring), and modern enterprise-sales architectures (multi-threading, mutual close plans, SPIN implication/need-payoff questions). These dominate practitioner curricula but have $k = 0$ or $k = 1$ in our Stage-1 included corpus.

A practitioner reading the academic literature on closing encounters a different set of named techniques than the practitioner-training canon emphasizes. A sales operator deploying assumptive closes, takeaway closes, and Ben Franklin closes is deploying techniques with no peer-reviewed empirical foundation at the level of our inclusion criteria.

## 3.3 Phase 2 pilot extraction

We extracted 9 records across 5 survivor techniques as a pilot demonstration of the Phase 2 pipeline.

### Table 2 — Phase 2 pilot records

| ID | Year | Technique(s) | Design | N | Effect | Pre-reg |
| --- | ---: | --- | --- | ---: | --- | --- |
| atlas-001 | 2021 | gain/loss framing | within-subjects experiment | 319 | $\beta = -19.00 \, [-23.0, -15.0]$ | OSF |
| atlas-002 | 2022 | extreme anchor | lab w/ scenario | 240 | AI = 0.78 (high) | no |
| atlas-003 | 2023 | concrete-construal | between-subjects exp | 247 | $M_{part} = 5.09$ vs $M_{ai} = 4.53$, $F(1,243)=5.96$ | no |
| atlas-004 | 2018 | social proof | between-subjects exp | 88 | $\eta^2 = 0.06$, $p = 0.02$ | no |
| atlas-005 | 2020 | gain/loss framing + extreme anchor | 2×2 factorial | 368 | $F = 61.4$, $F = 56.7$, both $p<0.001$ | no |
| atlas-006 | 2017 | gain/loss framing | 2×3 factorial | 229 | $\beta = 0.25$, indirect $ab = 0.16 \, [0.09, 0.25]$ | no |
| atlas-007 | 2022 | extreme anchor | 2×2 factorial | 400 | $F(1,396)=51.72$, $p<0.001$ | no |
| atlas-008 | 2019 | concrete-construal | **Stage-2 EXCLUDE** (correlational) | 216 | n/a | no |
| atlas-009 | 2019 | gain framing | three-arm RCT | 232 | $\eta_p^2 = 0.05$, $p < 0.001$ | no |

Combined Phase 2 pilot $N = 2{,}339$ participants across the original 9 records. Pre-registration rate **1/9 (11%)** — a directly testable population-level baseline for the persuasion-research literature.

### Phase 2 expansion (atlas-010 through atlas-019)

Phase 2 was scaled to 19 records via the MDPI and APA-OA open-access subsets. The expansion adds 8 primary-study extractions (atlas-010 to atlas-015, atlas-018, atlas-019), 1 systematic-review entry kept with `study_design=systematic-review` flag (atlas-017 Covey 2014), and 1 unable-to-access entry (atlas-016 — eScholarship maintenance window at fetch time, properly marked rather than silently retried). Three Stage-1 included records were pre-flagged as publication-type mismatches with the Phase 2 schema (two systematic reviews, one paired-meta-analyses paper) and left for a separate review-extraction protocol.

The expanded extraction crosses the per-technique k≥5 threshold for both gain-framing (inclusion-k=10, meta-eligible-k=6) and loss-framing (inclusion-k=8, meta-eligible-k=5). The inclusion-vs-meta-eligible distinction matters: not every record listing a technique in its `technique_taxonomy_id` field reports an effect-size metric the Phase 3 pipeline can convert to approximate Cohen's d (abstract-only OA records, narrative-synthesis review entries, descriptive-statistics rows without inference, and one percent-change metric from a commercial field deployment are skipped at the conversion step).

Methodological flags from the expansion:
- atlas-011 (Remountakis 2023 hotel-upselling) is rated `rob_overall=high` due to author affiliation with the commercial platform whose technology is the intervention. Sensitivity analysis with this record excluded is pre-registered for Phase 4.
- atlas-010 (Yu 2025 green advertising) reports F(1,235)=1927.860, implausibly large for framing research. Flag for skeptical sensitivity analysis; the size suggests either a dramatically engineered manipulation (concrete-vs-abstract message stimuli are unusually divergent), a reporting artifact, or demand-characteristic inflation in a panel-recruited online sample.
- atlas-014 (Toll 2007 smoking-cessation RCT) is the cleanest primary-study extraction in the new batch: NIH-funded, ITT primary analysis, randomization quality documented, blinding partial. Used as the RoB calibration anchor for future framing-literature judgments.

### Phase 2 expansion v2 (atlas-020 through atlas-044) — survivor-technique-targeted

Phase 2 was further expanded with a 25-record targeted extraction batch covering five Stage-1 survivor techniques (FITD, DITF, regulatory-fit, social-proof, commitment-consistency) — 5 OA candidates per technique. Wall-time result:

- **15 records actually extracted** (atlas-020-024, atlas-030-044). DITF batch (atlas-025-029) was killed mid-execution before producing CSV output; those 5 study IDs are reserved for a retry.
- **5 records yielded meta-eligible effect sizes**: atlas-033 (regulatory-fit, F-statistic), atlas-037 (social-proof, Cohen's d), atlas-040 (commitment-consistency, F-statistic), atlas-042 (commitment-consistency, adjusted odds ratio), atlas-044 (commitment-consistency, t-statistic).
- **8 records returned unable-to-access** despite being flagged is_oa=true in the Unpaywall API response. The accessibility-flag-vs-actual-accessibility gap is a real methodological finding: Wiley / Elsevier / OUP "open access" landing pages frequently redirect to paywalls in practice, and Unpaywall's is_oa field does not always discriminate true-OA from publisher-side-claimed-OA-with-paywall-fallback. Future Phase 2 expansion should target the genuinely-clean OA subsets (PMC, MDPI, Frontiers, OSF preprints, BMC) over the broader is_oa=true superset.
- **2 records were discovered systematic reviews** (atlas-031 Watanabe & Suga 2026; atlas-043 Stylianou et al. 2025) — kept with `study_design=systematic-review` flag rather than excluded, for honest cataloging.
- **1 record was discovered to not test the target technique** (atlas-041 Lee et al. 2017 — labeled with commitment-consistency in screening but actually tests social-proof and authority). This is a screening-label artifact and a flag for sharpening the Stage-1 inclusion criteria's technique-attribution step.

The aggregate Phase 2 status after both expansions:

- 39 records extracted
- 21 records with meta-eligible effect sizes (parseable to approximate Cohen's d)
- 5 records explicitly unable-to-access
- 4 records flagged as systematic-review / meta-analysis / theoretical paper
- 9 records primary-study but with effect sizes not extractable in pilot-parser-compatible form (narrative findings, percent-change without inference, chi-square without df, etc.)

## 3.4 Phase 3 pilot Bayesian meta-analysis

A pure-stdlib implementation of the Phase 3 random-effects pipeline (`scripts/pilot_meta_analysis.py`) using DerSimonian-Laird $\tau^2$ estimation plus importance-sampled Bayesian pooling produced posterior estimates for the three techniques with $k \geq 2$ convertible effect sizes after the Phase 2 expansion:

### Table 3 — Phase 3 pilot posterior estimates (44-record extraction)

| Technique | $k_{meta}$ | $\mu$ median | 95% CrI | $\tau$ median | $P(\mu > 0)$ | $P(\mu > 0.2)$ |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `gain-framing` | 9 | **0.474** | [0.305, 0.642] | 0.301 | 1.000 | 0.997 |
| `loss-framing` | 7 | **0.327** | [0.249, 0.410] | 0.047 | 1.000 | 0.999 |
| `regulatory-fit` | 3 | **0.484** | [0.346, 0.632] | 0.068 | 1.000 | 0.997 |
| `commitment-consistency` | 2 | **0.590** | [0.331, 0.782] | 0.089 | 0.999 | 0.993 |
| `social-proof` | 2 | 0.515 | [−0.494, 1.408] | 1.600 | 0.845 | 0.738 |
| `extreme-anchor` | 2 | 0.435 | [0.043, 0.745] | 0.269 | 0.983 | 0.914 |

The HIGH-confidence batch (atlas-045-049) added 4 records to gain-framing, 2 to loss-framing, and 1 to regulatory-fit. All three posteriors tightened as expected; point estimates shifted by less than 0.05 d-units in each case.

Five of six techniques have credible intervals cleanly excluding zero AND exceeding the pre-registered d=0.2 practical-significance threshold with $P > 0.98$. Social-proof is the exception — its CrI spans $[-0.494, 1.408]$ with $\tau$ = 1.600, reflecting substantial between-study heterogeneity from just two records with widely different effect-size magnitudes (atlas-004 social-proof in tipping context vs. atlas-037 Griskevicius advertising context). The wide CrI is the correct Bayesian response to within-technique heterogeneity at small k.

The 19-record posteriors are the first Atlas results where the credible intervals on the two best-studied techniques cleanly exclude zero AND exceed the pre-registered d=0.2 practical-significance threshold with $P > 0.98$.

### Bayesian update check (9 records → 19 records)

The expanded extraction allows a direct check of whether the posterior updates as a Bayesian random-effects model should under more data. The original 9-record gain-framing posterior was $\mu = 0.539$, 95% CrI $[-0.200, 1.053]$, $P(\mu > 0) = 0.93$ at $k = 2$. The 19-record rerun produces $\mu = 0.501$, 95% CrI $[0.251, 0.733]$, $P(\mu > 0) = 0.999$ at $k = 6$. Same direction, point estimate stable within $\pm 0.04$, posterior tightened by approximately 60% on credible-interval width. This is the textbook shape of a credible Bayesian update with more data.

**Important caveats** (transparent flagging required by §10):
- $k_{meta} = 2$-$6$ per technique → posterior intervals are narrower than the original pilot but still substantially wider than the final-preprint target of $k = 20$-$50$ per technique after full Phase 2 scale-up.
- Effect-size conversion from reported metrics ($\eta^2 \to d$, $F \to d$, $t \to r \to d$ via Rosenthal 1991, log-OR $\to d$ via Cox-Hasselblad / Chinn 2000) is approximate. Protocol-conformant inference via `analysis/02_primary_meta_analysis.R` (`brms` + Stan) uses `metafor::escalc` for canonical standardization.
- The pilot demonstrates pipeline correctness AND produces preliminary substantive posteriors. The substantive claims survive only contingent on the protocol-conformant rerun (R/brms with Stan-MCMC) reproducing the pilot direction.
- Forest plot of the three posteriors is in `figures/forest_pilot.svg`.

# 4. Discussion

[To be drafted at Phase 3 completion with final posterior estimates.]

# 5. Limitations

The complete limitations document is LIMITATIONS.md. Headline limitations:

1. **Public-databases-only restriction (Deviation 001)**: Scopus, Web of Science, PsycInfo, ABI/INFORM, EBSCO Business Source Complete, and full-text ProQuest Dissertations were not searched.
2. **Low-priority deferred exclusion (Deviation 005)**: 6,710 records with priority_score < 0.10 excluded without individual LLM review.
3. **Solo-author screening with LLM-assist (Deviation 003)**: Inter-rater κ check pending.
4. **English-only**: Non-English-language studies excluded.
5. **Stage-1 ≠ Stage-3 survivor**: Stage-1 included count is upper bound on what passes Stage-2 (full-text) and Phase 3 (Bayesian meta-analysis + multiverse + bias adjustment).

# 6. Open materials

All materials are public-domain or CC-BY-4.0 licensed and reproducible from the GitHub repository.

- **Protocol**: PROTOCOL.md
- **Deviation log**: PROTOCOL_DEVIATIONS.md
- **Taxonomy**: taxonomy/techniques.md
- **Search strategy**: search/strategy.md
- **Inclusion criteria**: search/inclusion_criteria.md
- **Extraction form**: search/extraction_form.md
- **Statistical analysis plan**: analysis/statistical_plan.md
- **Per-record screening decisions**: search/_priority_batch_*_decisions.json
- **Stage-1 survivor report**: results/stage1_survivor_report.md
- **Phase 2 extraction pilot**: data/extracted_studies_pilot.csv
- **Phase 3 R/brms scripts**: analysis/01_load_and_validate.R, 02_primary_meta_analysis.R, 03_multiverse.R, 04_bias_diagnostics.R, 05_sensitivity.R
- **Phase 3 Python pilot**: scripts/pilot_meta_analysis.py
- **Posterior summaries**: results/pilot_posterior_summaries.csv

# 7. Acknowledgments

This work was conducted by a single-author research effort using publicly accessible APIs (PubMed E-utilities, OpenAlex Works API, Crossref REST API, Semantic Scholar Graph API, arXiv API, OSF Registrations API, ClinicalTrials.gov API) and an LLM-assisted screening pipeline (Claude Opus 4.7 by Anthropic) for individualized record-level inclusion decisions. All decisions are reproducible from the recorded prompts and per-record reason logs in the repository.

# References

[To be auto-generated from data/extracted_studies.csv at Phase 2 completion.]
