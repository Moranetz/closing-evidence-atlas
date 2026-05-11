# Limitations

This document is the comprehensive limitations section that will be carried into the final preprint. It covers methodological constraints, scope restrictions, and coverage caveats — all transparently disclosed per the pre-registered protocol.

## 1. Coverage limitations

### 1.1 Public-databases-only restriction (Deviation 001)

The pre-registered protocol listed 9 databases. Lack of institutional subscription access required restricting primary execution to publicly accessible APIs: PubMed (NLM E-utilities), OpenAlex Works API, Semantic Scholar Graph API, Crossref REST API, arXiv API, OSF Registrations, AEA RCT Registry (web), ClinicalTrials.gov API.

**Databases dropped from primary execution:** Scopus, Web of Science (SSCI), PsycInfo (APA), ABI/INFORM Complete, EBSCO Business Source Complete, ProQuest Dissertations and Theses full-text.

**Estimated coverage gap:** 5–15% of historical (pre-2000) marketing-journal records and a similar fraction of grey literature. OpenAlex and Semantic Scholar overlap heavily with Scopus and Web of Science via DOI resolution; the marginal gap is likely smaller in practice but cannot be precisely characterized without comparison runs against the paid databases.

**Mitigation:** Forward and backward citation chasing of included studies via OpenAlex and Crossref citation graphs (Phase 2). Hand-search of top journals in marketing and consumer behavior over the last decade (Phase 2).

### 1.2 English-language-only

Studies published in languages other than English were excluded per pre-registered eligibility criterion § 4.7. This biases the corpus toward anglosphere persuasion research. Cross-cultural and non-anglosphere closing-research is underrepresented.

### 1.3 Time horizon 1970–present

Studies published before 1970 were excluded. This excludes the foundational compliance-and-influence literature in the 1950s–1960s (early Milgram, Asch, Festinger), although that work is well-known and would not change the closing-technique audit conclusion.

### 1.4 No commercial sales-call corpora

The Atlas analyzes peer-reviewed empirical literature. It does not analyze proprietary commercial sales-call datasets (Gong, Chorus, Outreach, ZoomInfo) — those exist outside the academic publication record. Findings about real-world sales-call frequencies of techniques can be made only through such corpora. Reported in the **Future Work** section of the preprint.

## 2. Screening limitations

### 2.1 Solo-author screening with LLM-assisted re-screen (Deviation 003-adjacent)

The Cochrane / Campbell standard methodology requires two independent screeners. This project used a single human reviewer (Marion Moranetz) plus LLM-assisted individualized screening (Claude Opus 4.7) against the pre-registered inclusion criteria. The two streams of decisions are tracked separately in the `screener` field of `search/screening_stage1.csv`.

**Mitigation:** A 100-record stratified-random calibration set is available for inter-rater κ verification at any time. The acceptance threshold is κ ≥ 0.70 per PROTOCOL.md § 13.1. Run `scripts/compute_kappa.py` after a human screener has independently classified `search/calibration_sample_blind.csv`.

### 2.2 Low-priority deferred exclusion (Deviation 005)

6,710 records (57% of the corpus) with priority_score < 0.10 were excluded heuristically without individual LLM review. The priority score is a weighted combination of venue tier, allowlist-token density in title/abstract, methodology signal, and provenance multiplier.

**Empirical justification:** Across 8 LLM-screened priority batches, include rate trajectory was:

| Score range | N | Include rate |
| --- | ---: | ---: |
| 1.18–1.60 | 100 | 95% |
| 0.86–1.18 | 100 | 92% |
| 0.74–0.86 | 100 | 69% |
| 0.55–0.74 | 100 | 86% |
| 0.49–0.55 | 100 | 72% |
| 0.45–0.49 | 100 | 77% |
| 0.43–0.45 | 100 | 43% |
| 0.40–0.43 | 100 | 30% |
| < 0.10 (deferred) | 6,710 | extrapolated < 5% |

The trajectory shows include rate collapses below score 0.42. Expected include rate at the < 0.10 tier is < 5%, meaning the expected number of missed includes is < 335. This is reported as a coverage caveat rather than a mitigation.

**Mitigation:** Sensitivity analysis at the Phase 3 preprint stage will report whether survivor classification changes under alternative exclusion thresholds (0.05, 0.15) per PROTOCOL § 9.6.

### 2.3 Heuristic-first-pass exclusion (Deviation 004)

1,228 records (10% of the corpus) were excluded by high-precision heuristic rules (Heuristic v1 + v2) before LLM screening. Both heuristic versions were validated at 100% precision against the LLM-screened calibration set (zero disagreements on the records the heuristic flagged for exclusion). The risk of false negatives is bounded by the calibration check.

## 3. Methodological limitations specific to this domain

### 3.1 Practitioner-named technique boundaries are fuzzy

Many practitioner techniques overlap conceptually. "Calibrated questions" (Voss) maps largely to "open questions" in Motivational Interviewing (OARS framework). "Mirroring" (Voss) overlaps with "reflection" (MI), "verbal repetition" (cognitive defusion), and "active listening" (counseling).

The Atlas taxonomy treats these as separate entries because the practitioner literature treats them separately. The eventual meta-analytic analysis will surface where these distinctions matter empirically and where they collapse. See `taxonomy/voss_mi_mapping.md` (drafted in Phase 2).

### 3.2 "Technique" is not a uniform construct

The 39 cataloged techniques range from highly specific sequential procedures (FITD, DITF, lowball, TNA) to broad psychological mechanisms (regulatory fit, construal level, anchoring). A study that experimentally manipulates a specific FITD procedure produces evidence-of-FITD that is methodologically different from a study that measures regulatory-fit-mediated message processing.

The Atlas reports these uniformly at Stage-1 to characterize the literature landscape but reports them separately at the per-technique level in Phase 3.

### 3.3 Population is heterogeneous

Per eligibility criterion § 2.1, the population is "decision-makers in a real or simulated commercial decision-making setting." This includes:

- Buyers in B2C settings (most behavioral-marketing literature)
- Buyers in B2B settings (much smaller literature)
- Compliance subjects in field experiments (charitable donation, blood donation, voter turnout, hand hygiene)
- Experimental participants in lab compliance and framing studies (students, MTurk workers)
- Real sales operators (very limited primary-study literature)

This is a feature of the literature, not a defect of the Atlas. Phase 3 will report per-technique heterogeneity (`tau`) and moderator analysis on B2B/B2C, transactional/consultative, and channel.

### 3.4 Outcomes are heterogeneous across studies

Studies in the corpus measure compliance, conversion, willingness to pay, willingness to buy, donation rate, donation amount, attitude change, behavioral intention, time-to-purchase, and post-purchase satisfaction. These are not interchangeable. Phase 3 effect-size standardization (Hedges' g or log-OR per § 7.3) handles this for pooling but does not eliminate construct-level heterogeneity.

### 3.5 Risk of bias in primary studies

Many compliance-and-influence studies were conducted decades ago, before modern pre-registration norms. Substantial publication bias is expected. The three-parameter selection model and PET-PEESE adjustment in Phase 4 are designed to surface this.

## 4. Specific limitations of the included-set characterization (as of Stage-1)

### 4.1 Stage-1 included ≠ Stage-3 survivor

The 572 Stage-1 included records are records whose **title and abstract** suggest eligibility. Stage-2 full-text screening typically drops 60–80% of Stage-1 includes for methodological reasons (no behavioral outcome reported, unmeasurable effect size, design mismatch, study population mismatch). The expected final included set after Stage-2 is 115–230 primary studies.

After Stage-3 Bayesian meta-analysis + multiverse + publication-bias adjustment, the survivor list is typically further reduced. Final survivors are reported in the preprint, not in this Stage-1 document.

### 4.2 The DESERT classification is conservative

The 15 techniques with zero Stage-1 includes (DESERT category) are conservatively classified based on public-databases-only search. Some DESERT techniques may have evidence in Scopus / Web of Science / PsycInfo, and some may have evidence under a different name (e.g., the "summary close" might be tested under "summary message" or "summary statement of need-payoff"). Phase 2 will attempt forward-citation chasing on the meta-analyses and practitioner-cited papers to find any unindexed studies.

### 4.3 Open-access accessibility for Phase 2 (Phase 1.5 accessibility report)

Of the 572 Stage-1 includes, 141 (25%) have a retrievable open-access PDF URL via Unpaywall and are accessible for autonomous Phase 2 extraction without external credentials. The remaining 431 records (75%) require either (a) institutional library access by Marion, (b) author-correspondence, or (c) extraction from title + abstract metadata only with documented coverage caveat. See `results/phase15_accessibility_report.md`.

## 5. What the Atlas is not

- Not a sales-training manual.
- Not a closing-script generator.
- Not a substitute for practice.
- Not a final survivor list — that requires Phase 3 to complete.
- Not a validation of any specific commercial sales-training program.
- Not a substitute for direct A/B testing on a real sales pipeline.

## 6. Honest worst-use cases

The Atlas can be misused to:

- Cherry-pick techniques whose effect size and credible interval support a preferred operating practice while ignoring the heterogeneity moderators.
- Dismiss DESERT techniques as ineffective when the correct conclusion is "untested at the level of these inclusion criteria."
- Generalize population-level effect sizes to individual sales operators or specific deals — the Atlas's effect sizes are population-average, not individual.

These misuses are anticipated and pre-emptively flagged in the preprint's discussion section.
