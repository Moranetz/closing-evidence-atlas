# Executive Summary

A pre-registered empirical audit of sales-closing techniques. Phase 1 (Stage-1 screening) complete. Phase 2 (extraction) at **44 records** across Frontiers + IRSP + MDPI + APA-OA + survivor-technique-targeted + HIGH-confidence PMC subsets. **Six per-technique posteriors**: gain-framing (k=9 μ=0.474), loss-framing (k=7 μ=0.327), regulatory-fit (k=3 μ=0.484), commitment-consistency (k=2 μ=0.590), extreme-anchor (k=2 μ=0.435), social-proof (k=2 μ=0.515). Five of six have credible intervals cleanly excluding zero AND exceeding the d=0.2 practical-significance threshold with P>0.98. Sensitivity analyses (`scripts/sensitivity_analysis.py`) confirm posterior stability under high-RoB exclusion and log-OR-conversion exclusion; one leverage flag on gain-framing's atlas-009 (Δμ=-0.132 in leave-one-out — needs re-extraction). OA-extractability classifier (`scripts/classify_oa_extractability.py`) shows only 8 HIGH-confidence OA records remain unextracted — Phase 2 has saturated the clean-OA subset. Production R/brms run pending Marion-action on R/brms/cmdstanr install.

## The premise

Sales-closing literature is mostly folklore. Hundreds of named techniques are taught with high confidence in commercial training programs. The empirical foundation under those techniques has never been comprehensively audited.

This project does the audit.

## The pipeline

- 39 named closing techniques cataloged from practitioner literature (Cialdini, Voss, Sandler, Hopkins, Rackham, Dixon, Belfort, Tracy)
- 7 public databases systematically searched (PubMed, OpenAlex, Crossref, Semantic Scholar, arXiv, OSF Registrations, ClinicalTrials.gov)
- 11,785 unique records identified after deduplication
- 8,839 records explicitly classified at Stage-1 screening
- Decisions made by a combination of high-precision heuristic exclusion (100% precision against calibration LLM), individualized LLM-assisted screening (901 records), and pre-registered low-priority deferred exclusion (6,710 records)
- 572 records included for Stage-2 full-text screening
- 141 of those (25%) are open-access with a retrievable PDF — accessible for autonomous full-text screening and extraction
- All deviations from the pre-registered protocol are transparently logged

## The headline finding

Of 39 named closing techniques in the practitioner taxonomy:

- **14 techniques (36%) have ≥ 5 Stage-1 included studies** — eligible for Phase 3 Bayesian meta-analysis. They cluster heavily on framing (gain/loss), compliance (FITD, DITF, lowball, TNA), and social-cue (reciprocity, social proof, authority, scarcity).
- **10 techniques (26%) have 1–4 studies** — too few for meta-analysis. Reported descriptively.
- **15 techniques (38%) have ZERO peer-reviewed empirical studies** — the empirical deserts.

The deserts include named techniques taught with confidence in modern sales-training programs: **assumptive close, alternative-choice close, summary close, trial close, takeaway close, Ben Franklin close, sharp-angle close, puppy-dog close, mutual close plan, multi-threading, isolate-the-objection, reverse-objection, accusation audit, SPIN implication question, SPIN need-payoff question, mirroring, bracketing.**

This is not a claim that these techniques are ineffective. It is a claim that they have not been tested at the level of the pre-registered inclusion criteria — peer-reviewed randomized or quasi-experimental design with a behavioral outcome.

## Why the gap matters

The dominant techniques in the academic empirical literature are not the techniques most prominent in modern sales-training programs.

- Sales-training programs lead with **structural closes** (assumptive, alternative-choice, summary, trial, takeaway, puppy-dog) and **negotiation moves** (Voss's calibrated questions, accusation audits, mirroring, bracketing).
- The academic empirical literature concentrates on **compliance and framing** mechanisms (FITD, DITF, gain/loss framing, lowball, regulatory fit, social proof, reciprocity).
- The two literatures barely overlap.

A practitioner who reads the academic literature on closing will encounter a different set of techniques than the practitioner literature emphasizes. A sales operator deploying assumptive closes and takeaway closes is deploying techniques with no peer-reviewed empirical support — not necessarily ineffective, but unvalidated.

## What Phase 2 and Phase 3 will produce

- Phase 2 — extract effect size, sample size, design, technique-taxonomy mapping, and risk-of-bias rating for each Stage-2-passing study. **Status: 19 records extracted (Frontiers + IRSP + MDPI + APA-OA subsets).** Per-technique k counts: gain-framing 10, loss-framing 8, extreme-anchor 3, concrete-construal 3, social-proof 3, regulatory-fit 1, plus 6 techniques at k=1 from one multi-technique extraction (atlas-011). Expected ~115–230 final included studies after Stage-2 attrition.
- Phase 3 — per-technique Bayesian random-effects meta-analysis with weakly-informative priors, multiverse-specification robustness across 486 reasonable analytical decisions, publication-bias diagnostics (funnel plot, Egger, p-curve, three-parameter selection model, PET-PEESE).
- Phase 4 — survivor classification across five pre-registered criteria. The output is a credibility-weighted-survivor list with effect-size estimates, posterior intervals, and explicit flagging of selection-fragile techniques.

## What the Atlas is not

- Not a sales-training manual.
- Not a closing-script generator.
- Not a substitute for practice.
- Not a final survivor list — that requires Phase 3 to complete.

## Coverage caveats

- **Public-databases-only.** Scopus, Web of Science, PsycInfo, and EBSCO Business Source Complete were not searched. Coverage gap estimated at 5–15% of historical marketing-journal records. Reported transparently in the final preprint (Deviation 001).
- **English-only.**
- **Solo-author with LLM-assisted re-screen.** Inter-rater κ check available at any time using the 100-record calibration set (Deviation 003).
- **Low-priority deferred exclusion of 6,710 records** with priority_score < 0.10 (Deviation 005). Empirical justification: LLM-screened include rate falls below 5% in this score band based on observed trajectory.

## The honest bottom line

The literature on sales closing is empirically uneven. A small set of compliance-and-framing techniques has accumulated substantial primary-study evidence. A larger set of practitioner-named techniques has none. Phase 3 will determine which of the well-studied techniques actually produces effects that survive multiverse-specification and publication-bias adjustment — and which were artifacts of selective reporting and small-sample noise.

The first sales-closing audit at this scale and methodological rigor lives in this repo. Read the [PROTOCOL.md](PROTOCOL.md) for what was pre-registered, [PROTOCOL_DEVIATIONS.md](PROTOCOL_DEVIATIONS.md) for every change, and [results/stage1_survivor_report.md](results/stage1_survivor_report.md) for the per-technique evidence-base summary that emerged.
