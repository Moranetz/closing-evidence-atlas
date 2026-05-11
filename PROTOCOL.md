# Closing Evidence Atlas — Pre-Registered Systematic Review and Bayesian Meta-Analysis Protocol

**Title:** A pre-registered systematic review and Bayesian meta-analysis of empirically tested sales-closing techniques.

**Authors:** Marion Moranetz (sole author, this draft).

**Date drafted:** 2026-05-10. **Status:** Pre-registration draft v0.2 (after Deviation 001 — public-databases-only restriction; see `PROTOCOL_DEVIATIONS.md`). Not yet posted to OSF; Atlas-G0 implicitly approved at "lets begin" message of 2026-05-10.

**Intended registration platform:** OSF Registries (https://osf.io/registries) — Standard Pre-Registration template.

**Conformance:** PRISMA 2020 reporting guideline; PROSPERO eligibility (will register on PROSPERO concurrent with OSF).

---

## 1 · Background and rationale

Sales closing is a high-stakes commercial behavior that has been the subject of practitioner-authored books for over a century (e.g., Hopkins 1980; Rackham 1988; Cialdini 1984; Voss 2016; Dixon & Adamson 2011; Sandler 1996). Across this corpus, hundreds of named "closing techniques" are described — among them the **assumptive close**, the **alternative close**, the **summary close**, the **takeaway close**, the **trial close**, the **Ben Franklin close**, the **puppy-dog close**, the **sharp-angle close**, the **calibrated-question close**, and many others.

These techniques are taught with high confidence in commercial training programs but the underlying empirical foundation has never been comprehensively audited. The few existing reviews (Schwepker 2003; Roman & Iacobucci 2010; Sherer 2013) are scoped to single sub-domains (e.g., ethical persuasion, retail, telesales) and pre-date both modern meta-analytic standards and the open-science reform movement (Simonsohn et al. 2014; Munafò et al. 2017).

This pre-registered review will:

1. Catalog every named sales-closing technique appearing in the practitioner literature (the **taxonomy step**).
2. Identify all empirical studies (randomized, quasi-experimental, observational, field-experimental) testing the effect of any cataloged technique on a closing-relevant outcome.
3. Extract effect sizes, study quality indicators, and contextual moderators.
4. Pool effects per technique using Bayesian random-effects meta-analysis with weakly informative priors.
5. Audit publication bias (funnel plot asymmetry, Egger's test, p-curve analysis, three-parameter selection model).
6. Run multiverse / specification-curve analyses (Steegen et al. 2016; Simonsohn et al. 2020) over reasonable analytical decisions.
7. Report a final ranked list of closing techniques by **credibility-weighted effect size** (CWES), with associated uncertainty intervals.

---

## 2 · Research questions

**Primary RQ-1.** Among named sales-closing techniques described in the practitioner literature, which have credible empirical support — defined as: at least one preregistered or independently replicated study with a standardized effect size whose 95% credible interval excludes zero in the practitioner-claimed direction?

**Primary RQ-2.** When effects are pooled via random-effects meta-analysis with weakly-informative priors, what is the posterior distribution of the population effect for each technique? Which techniques have posterior medians and 95% credible intervals that survive a pre-registered robustness multiverse?

**Secondary RQ-3.** What contextual moderators (B2B vs. B2C; transactional vs. consultative; in-person vs. phone vs. digital; cultural region; immediate vs. delayed close) systematically modify technique efficacy?

**Secondary RQ-4.** What is the magnitude of evidence of publication bias in this literature? Does the survivor list shrink under three-parameter selection models?

**Descriptive RQ-5.** What proportion of named techniques in the practitioner literature have *zero* empirical studies satisfying our inclusion criteria?

---

## 3 · Hypotheses

This is fundamentally a **descriptive** project — its purpose is to characterize the empirical foundation of a literature, not to test a specific causal claim. We therefore pre-register **directional priors** rather than directional hypotheses, with one exception (H1).

**H1 (registered prediction).** A majority (≥ 50%) of named sales-closing techniques in the practitioner literature will have **zero** randomized or quasi-experimental studies satisfying our inclusion criteria. Pre-specified rationale: prior coverage estimates from adjacent fields (Roman & Iacobucci 2010; Schwepker 2003) suggest the empirical literature is dominated by a small subset of well-studied techniques (e.g., reciprocity, scarcity, social proof) while the long tail of named techniques rests on practitioner anecdote.

**Prior beliefs (descriptive, not hypothesis-tested).**
- We expect Cialdini's six principles, calibrated questions / labeling (Voss-MI overlap), and concrete-language framing to have the strongest empirical support.
- We expect aggressive / high-pressure techniques (e.g., **takeaway close**, **sharp-angle close**) to show effect heterogeneity that is large and modulated by relationship duration.
- We expect publication bias to be substantial in this literature.

These priors are recorded for reflexivity. They will not influence inclusion decisions or analytic choices.

---

## 4 · Eligibility criteria

### 4.1 Population
Studies whose participants are decision-makers in a real or simulated commercial decision-making setting. Includes: customers in B2C settings; buyers in B2B settings; experimental participants in simulated commercial roles; participants in field experiments where a sales-relevant decision is the outcome.

**Excluded:** purely intra-organizational influence (negotiation between teammates with no exchange of value); political persuasion; clinical / therapeutic persuasion (use of MI in medical settings) — *unless* the technique-level mechanism is identical to a sales-named technique and the study explicitly draws the parallel. Borderline cases will be resolved by consensus coding (see §7.2).

### 4.2 Intervention
Any operationalization of a named closing technique drawn from the cataloged practitioner taxonomy (see `taxonomy/techniques.md`).

The intervention must be:
- **Specifically operationalized** — not merely "a persuasion attempt." The study must describe the manipulation with sufficient detail that we can map it to a single named technique.
- **Distinguished from a control** — either (a) a no-technique control, (b) an alternative-technique control, or (c) within-subject baseline.

### 4.3 Comparator
- **Active comparator** (alternative technique) — preferred for technique-vs-technique effect estimation.
- **Inactive comparator** (no-pitch / generic-pitch baseline) — required for absolute-effect estimation.

Both comparator types are eligible; effect sizes will be coded with comparator type as a moderator.

### 4.4 Outcomes

**Primary outcomes (eligible):**
- Close rate (binary: deal closed / not closed)
- Conversion rate (binary or proportional)
- Compliance rate (proportion accepting an offer or request)
- Contract value / revenue per deal (continuous)
- Cycle time (continuous, log-transformed)

**Secondary outcomes (eligible if reported alongside primary):**
- Customer-reported willingness to buy (Likert)
- Customer-reported trust / rapport (Likert)
- Behavioral intention measures (Ajzen 1991-shaped scales)

**Excluded outcomes:**
- Salesperson-reported confidence or perceived effectiveness (self-report only).
- Knowledge-test outcomes from sales training studies (does not measure closing behavior).

### 4.5 Study designs

**Eligible:**
- Randomized controlled trials (RCTs)
- Cluster-randomized trials
- Quasi-experimental field trials with clear treatment assignment
- Lab experiments with random assignment
- Field experiments / A-B tests with random or quasi-random assignment

**Excluded:**
- Pure observational studies without identification strategy (correlational)
- Single-case studies / case reports
- Pre-post designs without a control group
- Theoretical / conceptual papers

**Marginal (will be coded but flagged):**
- Quasi-experiments with strong identification (regression discontinuity, instrumental variables, difference-in-differences) — eligible but pooled separately as sensitivity analysis.

### 4.6 Time horizon
Publications from January 1970 through the search execution date (estimated 2026-05-15). The 1970 lower bound captures the post-Hopkins (1947) and post-Cialdini-PhD (1971) era when systematic study of compliance and influence emerged.

### 4.7 Language
English-language publications only. We acknowledge this is a limitation (introduces anglosphere skew); we will report on our PRISMA flow whether non-English studies appear in our database returns and were excluded for language.

### 4.8 Publication type
Peer-reviewed journal articles, peer-reviewed conference proceedings, and dissertations from accredited institutions. Working papers are eligible only if cited or replicated by a peer-reviewed source. Grey literature is otherwise excluded except where included in the publication-bias analysis (§9.4).

---

## 5 · Information sources and search strategy

See `search/strategy.md` for full search-string specifications. **Note: per Deviation 001 (`PROTOCOL_DEVIATIONS.md`), this protocol is restricted to publicly accessible databases due to lack of institutional subscription access.** The list below reflects the post-deviation state.

**Databases (executed in this order):**
1. PubMed (NLM E-utilities) — for behavioral-science studies tagged under MeSH terms for persuasion, compliance, salesmanship.
2. OpenAlex (Works API) — broad coverage (~250M papers); the primary replacement for the originally-listed Scopus and Web of Science.
3. Semantic Scholar (Graph API) — ~200M papers; complementary to OpenAlex; strong NLP-tagged metadata.
4. Crossref (REST API) — DOI-resolution + forward citation chasing.
5. arXiv (API) — preprints in CS/NLP relevant to persuasion modeling.
6. PsyArXiv (OSF API) — preprints in psychology / behavioral science.
7. SSRN (via Crossref + targeted Web search) — preprints in business / marketing.
8. OSF Registries (OSF API) — pre-registrations.
9. AEA RCT Registry (web) — registered randomized field trials.
10. ClinicalTrials.gov (API) — clinical persuasion / motivational-interviewing trials.
11. Google Scholar (via WebSearch tool, supplementary, ≤ 200 hits per technique-specific query) — citation chasing only.

**Originally listed but dropped (Deviation 001):** Scopus, Web of Science, PsycInfo, ABI/INFORM Complete, EBSCO Business Source Complete, ProQuest Dissertations full-text. Coverage gap relative to the original protocol is reported in LIMITATIONS.md.

**Hand-search:**
- Forward and backward citation chasing of all included studies (Cooper 2017).
- Reference lists of prior reviews (Schwepker 2003; Roman & Iacobucci 2010; Sherer 2013).
- Top journals in marketing and consumer behavior, last 10 years: *Journal of Marketing*, *Journal of Marketing Research*, *Journal of Consumer Research*, *Marketing Science*, *Journal of Personal Selling & Sales Management*, *Industrial Marketing Management*, *Journal of Consumer Psychology*, *Journal of the Academy of Marketing Science*.

**Open-source corpora and replications:**
- Many Labs / ManyBabies / Psychological Science Accelerator replication outputs filtered for persuasion / compliance.
- The "Persuasion For Good" corpus (Wang et al. 2019) and any derivative published analyses.
- Cornell ConvoKit — published papers using its corpora.

**Search execution:** all searches will be executed by Marion Moranetz in a single search session per database, with full search strings, hit counts, and date stamps recorded in `search/search_log.md`. Search results will be exported to RIS/CSV and deduplicated using the `revtools` R package.

---

## 6 · Study selection

**Stage 1 (title and abstract screening):** Two independent screeners (M. Moranetz + a second screener TBD — see §13 deviations) screen all unique records against the eligibility criteria. Disagreements resolved by discussion. If a second screener is not identifiable (likely, given solo-author constraint), single-screener with explicit calibration-set protocol (see §13). Inter-rater agreement target: Cohen's κ ≥ 0.70 on a 100-record calibration set.

**Stage 2 (full-text screening):** Identical procedure on full-text records.

**Reasons for exclusion** at full-text stage will be recorded per record per PRISMA 2020 guidance.

**Output:** PRISMA 2020 flow diagram in `search/prisma_flow.md`.

---

## 7 · Data extraction

### 7.1 Extraction form
See `search/extraction_form.md` for the full instrument. Summary of fields:

- Study identifier (DOI, year, authors, journal)
- Study design
- Sample size (total, per arm)
- Population characteristics (age, gender, sales setting, country)
- Technique tested (mapped to taxonomy)
- Operationalization details (verbatim excerpt where possible)
- Comparator type
- Outcome measure(s) (primary, secondary)
- Effect size (extracted as reported and converted to Cohen's d, log-OR, or risk ratio per outcome family — see §7.3)
- Variance / confidence interval / standard error
- Pre-registration status (yes / no / OSF link if available)
- Funding source / conflict of interest disclosure
- Risk of bias indicators (see §8)

### 7.2 Coding procedure
Two independent extractors per study where feasible (see §13 for solo-author deviation). Discrepancies resolved by re-reading the source paragraph. Calibration: 10 randomly selected studies double-extracted before main extraction begins; per-field agreement reported; sources of disagreement triaged and form revised before main extraction.

### 7.3 Effect-size standardization
- Continuous outcomes → Hedges' *g* (small-sample-corrected Cohen's d).
- Binary outcomes → log-odds-ratio (preferred); risk ratio reported for descriptive purposes.
- Mixed → converted following Borenstein et al. (2009), Chapter 7.
- Where standard errors are not directly reported, computed from F, t, χ², or reconstructed sample-size-and-effect tables.
- Studies that report only p-values without effect sizes will be coded as "effect size unrecoverable" and excluded from quantitative pooling but retained in the qualitative synthesis.

---

## 8 · Risk of bias

Per-study risk of bias assessed using design-appropriate tools:
- RCTs → Cochrane RoB 2.0 (Sterne et al. 2019)
- Quasi-experiments → ROBINS-I (Sterne et al. 2016)
- Observational with identification → adapted ROBINS-I

Each study scored on each domain (low / moderate / high / unclear). Inter-rater agreement reported. Risk-of-bias score will be a moderator in sensitivity analyses (§9.6) but will *not* drive exclusion at extraction time.

---

## 9 · Synthesis and analysis

### 9.1 Software
- R 4.4+ for primary analyses
- `brms` (Bürkner 2017) for Bayesian random-effects meta-analytic models
- `metafor` (Viechtbauer 2010) for sensitivity analyses and frequentist comparison
- `bayesplot` for posterior visualization
- `specr` and custom code for specification-curve analysis

All code will be public in `analysis/` upon Atlas-G3 approval. Random seeds fixed and reported.

### 9.2 Primary model (per technique)
Bayesian random-effects meta-analytic model:

```
y_i ~ Normal(theta_i, se_i)
theta_i ~ Normal(mu, tau)
mu ~ Normal(0, 0.5)            # weakly-informative on Hedges' g scale
tau ~ Half-Normal(0, 0.3)      # weakly-informative between-study SD
```

For binary-outcome techniques the same structure runs on log-OR scale with prior `mu ~ Normal(0, 0.7)`, `tau ~ Half-Normal(0, 0.5)`.

Estimands per technique:
- Posterior median of `mu` (population-average effect)
- 95% credible interval on `mu`
- Posterior probability that `mu > 0` in the practitioner-claimed direction
- Posterior median and 95% CI on `tau` (between-study heterogeneity)
- Prediction interval (Higgins, Thompson, Spiegelhalter 2009)

### 9.3 Moderator analyses (RQ-3)
Per-technique meta-regression on pre-specified moderators: B2B/B2C, in-person/phone/digital, transactional/consultative, region, mean participant age, year-of-study (recency).

Moderators are pre-specified; we will not search for moderators post hoc unless flagged transparently as exploratory (§13).

### 9.4 Publication-bias diagnostics
- Funnel plot per technique with ≥ 10 studies.
- Egger's regression test (Egger et al. 1997).
- p-curve analysis (Simonsohn, Nelson, Simmons 2014).
- Three-parameter selection model (Vevea & Hedges 1995) — adjusts for selection conditional on significance.
- PET-PEESE corrections (Stanley & Doucouliagos 2014) reported as sensitivity.

A technique whose effect estimate falls below practical significance under PET-PEESE or three-parameter selection adjustment will be flagged in the survivor list as **selection-fragile**.

### 9.5 Multiverse / specification-curve analysis (RQ-2 robustness)
For each technique with ≥ 5 studies, we run a multiverse over reasonable analytical decisions:
- Inclusion: all-eligible vs. low-RoB-only vs. preregistered-only
- Effect-size estimator: Hedges' g vs. log-OR (where convertible)
- Prior on `mu`: weakly-informative vs. flat vs. skeptical (Normal(0, 0.1))
- Outlier handling: no exclusion vs. studentized-residual-based exclusion vs. leave-one-out
- Heterogeneity prior on `tau`: Half-Normal(0, 0.3) vs. Half-Cauchy(0, 0.5) vs. truncated-Normal(0, 0.5)
- Comparator restriction: any comparator vs. inactive-only vs. active-only

Cross-product gives ≈ 162 analytical specifications per technique. Specification curve plotted with median, 90% interval, and proportion of specifications producing CI excluding zero.

A technique survives the multiverse if **≥ 80% of specifications produce a posterior 95% CI on `mu` that excludes zero in the practitioner-claimed direction**.

### 9.6 Sensitivity analyses
- Effect estimates excluding high-RoB studies.
- Leave-one-out per technique.
- Effect estimates restricting to post-2015 studies (post replication-crisis era).
- Effect estimates restricting to preregistered studies.
- Effect estimates restricting to direct conceptual replications (not first-tests).

### 9.7 Survivor definition (RQ-1)
A closing technique is **credibility-weighted-survivor (CWS)** if it satisfies all of:
1. ≥ 5 eligible primary studies after PRISMA filtering.
2. Random-effects posterior on `mu` has a 95% credible interval excluding zero in the practitioner-claimed direction.
3. Survives multiverse threshold (§9.5).
4. Effect remains practically significant (|posterior median *g*| ≥ 0.20 or |log-OR| ≥ 0.20) after PET-PEESE adjustment.
5. Effect not solely driven by studies funded by parties with commercial interest in the technique.

Techniques satisfying ≥ 4 of 5 criteria are flagged **CWS-borderline**.

---

## 10 · Stopping rule

The Atlas Phase 1 (search execution) is bounded by database returns through the search execution date. No adaptive stopping. Phase 2 (extraction) continues until all eligible records are extracted or until two-extractor agreement κ falls below 0.60 indicating coding form failure (in which case the form is revised and extraction restarts).

---

## 11 · Anticipated deviations and contingency plans

The principal investigator notes the following anticipated deviations from canonical Cochrane / Campbell methodology and pre-commits to handling each transparently in the final report.

**11.1 Solo-author single-screener risk.** Cochrane methodology requires two independent screeners. Solo-author projects mitigate this risk by: (a) explicit calibration set with κ reporting; (b) full-text screening of any borderline title-abstract record; (c) recorded second-pass screen of all excluded records by an LLM-assisted re-screen with disagreements adjudicated. The LLM-assisted re-screen is *additive* to single-human screening, not replacement, and is reported as a methodological deviation.

**11.2 LLM-assisted extraction.** Where studies report effect sizes ambiguously, LLM-assisted extraction (Claude or GPT-4-class) may be used to surface candidate values, *always* with human verification of the final extracted number against the source PDF. LLM-only extraction is forbidden.

**11.3 Pre-2000 effect-size reconstruction.** Older papers may report only F-statistics and degrees of freedom. Reconstruction follows Borenstein et al. (2009). Where reconstruction is ambiguous, the study is excluded from quantitative pooling.

**11.4 Newly identified techniques during extraction.** If extraction surfaces a technique not in our pre-registered taxonomy, we (a) add it to the taxonomy, (b) flag it in the deviation log, (c) include it in the meta-analysis, (d) report it explicitly as a post-hoc inclusion.

---

## 12 · Reporting and dissemination

**Primary output:** preprint deposited on OSF Preprints and PsyArXiv simultaneously with first public release of the repo.

**Secondary outputs:**
- PRISMA 2020 flow diagram + checklist
- Full extracted dataset (CSV) under CC-BY-4.0
- Analysis code (R, Python) under MIT
- Posterior samples per technique (RDS files)
- Specification-curve figures per technique
- Plain-language summary in `EXECUTIVE_SUMMARY.md` (Persuasion-Max voice)

**Journal target (post-preprint):** *Psychological Bulletin*, *Annual Review of Psychology*, or *Journal of Marketing Research*, in roughly that order. Decision deferred to post-G3.

---

## 13 · Pre-registered deviation log policy

This protocol is version-controlled in git. Any change after Atlas-G0 sign-off is logged in `PROTOCOL_DEVIATIONS.md` with: date, section affected, change, justification. All deviations are reported in the final preprint per PRISMA 2020 item 24c.

The protocol is binding once signed off. Changes after extraction begins are *strongly* discouraged and require justification stronger than "the data suggested otherwise."

---

## 14 · Conflicts of interest

The principal investigator (M. Moranetz) is concurrently applying for sales-adjacent commercial roles. This is disclosed. The investigator commits to:
- Not selectively highlighting techniques that support a personal sales narrative.
- Reporting null results, fragile-survivor results, and shrinkage-under-bias-adjustment results with equal prominence.
- Allowing the data to determine the survivor list.

The investigator has no financial relationship with any sales-training program, technique author, or proprietary methodology.

---

## 15 · Atlas-G0 sign-off requested

Mel reviews this protocol and either:
- Signs off → I commit it to git, post to OSF, and begin Phase 1 (search execution).
- Requests changes → I revise per her feedback and resubmit for sign-off.
- Pauses the project → state preserved; no further work until next signal.

Default if silent: I post a 24-hour notice in the next session and proceed if no further response. (See §4 of the Closer Foundation SERIES_PLAN.)
