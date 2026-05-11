# Stage-1 Survivor Report — Per-Technique Evidence Base

Auto-generated from `search/screening_stage1.csv` via `scripts/stage1_technique_summary.py`. Reflects screening state as of 2026-05-10.

## Headline numbers

- Techniques cataloged in taxonomy: **39**
- Techniques with ≥ 5 Stage-1 included studies (survivors): **14**
- Techniques with 1-4 studies (FRAGILE): **10**
- Techniques with 0 included studies (DESERT): **15**

This is the empirical landscape of the sales-closing literature at Stage-1 screening. The DESERT and FRAGILE categories collectively are direct evidence for RQ-5: a meaningful fraction of named techniques in the practitioner literature have essentially no peer-reviewed empirical foundation.

## Survivor techniques (≥ 5 Stage-1 includes)

Ranked by include count. These techniques have enough primary literature to proceed to Stage-2 full-text screening and ultimately to per-technique Bayesian meta-analysis.

| Technique | Cluster | Include | Uncertain | Exclude | Status |
| --- | --- | ---: | ---: | ---: | --- |
| `gain-framing` (Gain framing) | framing | 138 | 15 | 65 | DOMINANT LITERATURE |
| `loss-framing` (Loss-aversion framing) | framing | 112 | 19 | 65 | DOMINANT LITERATURE |
| `fitd` (Foot-in-the-door) | compliance | 105 | 3 | 158 | DOMINANT LITERATURE |
| `ditf` (Door-in-the-face) | compliance | 70 | 2 | 201 | DOMINANT LITERATURE |
| `regulatory-fit` (Regulatory fit) | framing | 47 | 30 | 127 | STRONG EVIDENCE |
| `social-proof` (Social proof) | social-cue | 47 | 11 | 186 | STRONG EVIDENCE |
| `concrete-construal` (Concrete-vs-abstract framing) | framing | 25 | 18 | 181 | STRONG EVIDENCE |
| `extreme-anchor` (Extreme anchor) | negotiation-anchor | 22 | 4 | 309 | STRONG EVIDENCE |
| `lowball` (Low-ball) | compliance | 21 | 1 | 351 | STRONG EVIDENCE |
| `commitment-consistency` (Commitment & consistency) | compliance | 18 | 8 | 232 | MODEST EVIDENCE |
| `authority` (Authority cues) | social-cue | 17 | 6 | 190 | MODEST EVIDENCE |
| `reciprocity` (Reciprocity) | social-cue | 14 | 19 | 556 | MODEST EVIDENCE |
| `scarcity` (Scarcity) | framing | 13 | 0 | 462 | MODEST EVIDENCE |
| `disrupt-then-reframe` (Disrupt-then-reframe) | compliance | 6 | 0 | 252 | MODEST EVIDENCE |

## Fragile-evidence techniques (1-4 Stage-1 includes)

These techniques have some empirical literature but below the pre-registered threshold for meta-analysis. They are reported descriptively in the final preprint with explicit caveats.

| Technique | Cluster | Include | Uncertain | Exclude |
| --- | --- | ---: | ---: | ---: |
| `anchor-with-range` (Range anchor) | negotiation-anchor | 4 | 3 | 222 |
| `labeling` (Affect labeling) | question-form | 4 | 4 | 273 |
| `liking` (Liking / similarity / rapport) | social-cue | 4 | 3 | 73 |
| `tna` (That's-not-all) | compliance | 4 | 0 | 442 |
| `calibrated-question` (Calibrated question) | question-form | 3 | 0 | 297 |
| `takeaway` (Takeaway close) | structural-close | 2 | 0 | 278 |
| `assumptive` (Assumptive close) | structural-close | 1 | 0 | 263 |
| `feel-felt-found` (Feel-felt-found) | post-objection | 1 | 2 | 136 |
| `precise-anchor` (Precise number anchor) | negotiation-anchor | 1 | 0 | 87 |
| `silence` (Strategic silence after offer) | closing-environment | 1 | 1 | 269 |

## Empirical deserts (0 Stage-1 includes)

These techniques are named extensively in the practitioner literature (Hopkins, Voss, Sandler, MEDDIC, Challenger Sale) but did not surface in our systematic search of public-databases-only literature. This is direct evidence that they have **no peer-reviewed empirical foundation** at the level of our pre-registered inclusion criteria. Discussed in PROTOCOL.md § 2 RQ-5.

| Technique | Cluster | Practitioner-claimed mechanism |
| --- | --- | --- |
| `accusation-audit` (Accusation audit) | question-form | per taxonomy |
| `alternative-choice` (Alternative-choice close) | structural-close | per taxonomy |
| `ben-franklin` (Ben Franklin / pros-and-cons close) | structural-close | per taxonomy |
| `bracketing` (Bracketing) | negotiation-anchor | per taxonomy |
| `isolate-and-conquer` (Isolate-the-objection) | post-objection | per taxonomy |
| `mirroring` (Mirroring (verbal repetition)) | question-form | per taxonomy |
| `multi-threading` (Multi-threading / champion-development) | closing-environment | per taxonomy |
| `mutual-close-plan` (Mutual close plan) | closing-environment | per taxonomy |
| `puppy-dog` (Puppy-dog close) | structural-close | per taxonomy |
| `reverse-objection` (Boomerang / reverse objection) | post-objection | per taxonomy |
| `sharp-angle` (Sharp-angle close) | structural-close | per taxonomy |
| `spin-implication` (SPIN implication question) | question-form | per taxonomy |
| `spin-need-payoff` (SPIN need-payoff question) | question-form | per taxonomy |
| `summary-close` (Summary close) | structural-close | per taxonomy |
| `trial-close` (Trial close) | structural-close | per taxonomy |

## Methodological notes

- DESERT classification is conservative: it reflects only what surfaced from public-databases-only search. Per Deviation 001, paid databases (Scopus, Web of Science, PsycInfo, EBSCO) were not searched; some DESERT techniques may have evidence in those databases.
- The Stage-1 included count for each technique is an upper bound on what passes Stage-2 (full-text screening); expected drop is 60-80%.
- Per PROTOCOL.md § 9.7, the survivor classification at the final preprint stage requires Bayesian random-effects meta-analysis with multiverse robustness; this Stage-1 survivor count is the *eligibility threshold for that analysis*, not the analysis itself.
