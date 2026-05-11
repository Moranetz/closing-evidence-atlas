# closing-evidence-atlas — Per-Repo Ultraplan

> Pre-registered Bayesian meta-analysis of empirically tested sales-closing techniques. The empirical foundation of the Closer Foundation series.

**Repo target:** `Moranetz/closing-evidence-atlas` (public, MIT for code, CC-BY-4.0 for protocol/data) · **Drafted:** 2026-05-10 · **Status:** Phase 0 in progress this session.

Parent: `~/Developer/closer-foundation/SERIES_PLAN.md`.

---

## 0 · Phase 0 — Foundations *(this session, ~1 day)*

✅ Completed in this session:
- Repo skeleton at `~/Developer/closing-evidence-atlas/`
- `PROTOCOL.md` — full pre-registration draft
- `search/strategy.md` — database list, search strings, hit-yield estimates
- `search/inclusion_criteria.md` — operational decision rules
- `search/extraction_form.md` — structured data instrument
- `analysis/statistical_plan.md` — Bayesian random-effects model spec, multiverse design, survivor classification
- `taxonomy/techniques.md` — pre-registered taxonomy v0.1 (35 techniques)
- This `PLAN.md`

Pending Atlas-G0 sign-off:
- [ ] Mel reads `PROTOCOL.md` and signs off
- [ ] OSF pre-registration submitted
- [ ] PROSPERO registration submitted (concurrent)
- [ ] `git init`, initial commit, push to **private** repo (public flip is at Atlas-G3)

---

## 1 · Phase 1 — Systematic search execution *(weeks 2–3)*

| Step | Output |
| --- | --- |
| 1.1 Execute search strings on each database per `search/strategy.md`. Record hit counts, dates, full strings. | `search/search_log.md` (verbatim record per database) |
| 1.2 Export results in RIS / CSV. Import to a Zotero collection. Apply `revtools` deduplication, then manual second pass. | Deduplicated record set |
| 1.3 Calibration set: random sample of 100 records double-screened. Compute κ. | `search/calibration_kappa.md` |
| 1.4 Title-abstract screen on full set. Flag borderline → full-text. | `search/screening_log.csv` |
| 1.5 Full-text screen on Stage-1 includes. Track exclusion reasons. | `search/screening_log.csv` |
| 1.6 PRISMA 2020 flow diagram. | `search/prisma_flow.md` |

**Approval gate Atlas-G1 (after Phase 1):** Mel reviews PRISMA flow, taxonomy lock-in (any new techniques surfaced in search), included-study count.

---

## 2 · Phase 2 — Data extraction *(weeks 4–5)*

| Step | Output |
| --- | --- |
| 2.1 Pilot extraction on 10 random studies. Compute per-field agreement. Revise form if needed. | `data/pilot_extraction.csv` + revision log |
| 2.2 Main extraction. Single extractor per study with LLM-assisted re-extraction for verification. | `data/extracted_studies.csv` (gitignored until G2) |
| 2.3 Effect-size standardization (Hedges' g / log-OR per § 7.3 of PROTOCOL). | `data/standardized_effects.csv` |
| 2.4 Risk-of-bias coding (Cochrane RoB 2.0 / ROBINS-I per § 8). | `data/rob_assessments.csv` |
| 2.5 Validation script run on all extractions. | `scripts/validate_extraction.py` output clean |

---

## 3 · Phase 3 — Primary meta-analysis *(week 6)*

| Step | Output |
| --- | --- |
| 3.1 Per-technique random-effects Bayesian model (`brms`). | `analysis/fits/<technique>.rds` |
| 3.2 Posterior summaries per technique. | `results/posterior_summaries.csv` |
| 3.3 Forest plots per technique. | `figures/forest_<technique>.pdf` |
| 3.4 Convergence diagnostics review. | `results/convergence_log.md` |

---

## 4 · Phase 4 — Multiverse + bias diagnostics *(week 7)*

| Step | Output |
| --- | --- |
| 4.1 Multiverse / specification-curve analysis per technique with ≥ 5 studies. | `figures/spec_curve_<technique>.pdf` + `results/multiverse_summaries.csv` |
| 4.2 Funnel plot, Egger's test per technique with ≥ 10 studies. | `figures/funnel_<technique>.pdf` + `results/egger_<technique>.csv` |
| 4.3 p-curve analysis per technique with ≥ 10 studies. | `results/pcurve_<technique>.csv` |
| 4.4 Three-parameter selection model + PET-PEESE. | `results/selection_<technique>.csv` |
| 4.5 Sensitivity analyses (low-RoB only, post-2015 only, pre-registered only, leave-one-out, industry-funded split). | `results/sensitivity_<technique>.csv` |
| 4.6 Survivor classification per § 8 of statistical plan. | `results/survivor_classification.csv` |

**Approval gate Atlas-G2 (after Phase 4):** Mel reviews survivor list before preprint draft begins. This is the first time real findings surface.

---

## 5 · Phase 5 — Preprint draft *(weeks 8–9)*

| Step | Output |
| --- | --- |
| 5.1 Manuscript draft conforming to PRISMA 2020. | `manuscript/atlas_v1.0.tex` (or .md) |
| 5.2 Per-technique one-page reports compiled to appendix. | `manuscript/appendix_per_technique.pdf` |
| 5.3 Plain-language `EXECUTIVE_SUMMARY.md` in Persuasion-Max voice. | `EXECUTIVE_SUMMARY.md` |
| 5.4 Public README in Persuasion-Max voice. Verified receipts only. | `README.md` |
| 5.5 LIMITATIONS.md — corpus-era, language-skew, single-author screening, technique-overlap caveats. | `LIMITATIONS.md` |

**Approval gate Atlas-G3 (after Phase 5):** Mel reads README aloud — voice check, receipt check. Iterate before public.

---

## 6 · Phase 6 — Public release *(week 10)*

| Step | Output |
| --- | --- |
| 6.1 Run preflight script: tests pass, notebooks execute end-to-end, lint clean, no TODO markers. | preflight green |
| 6.2 `gh repo create Moranetz/closing-evidence-atlas --public ...`. | repo public |
| 6.3 Deposit preprint to OSF Preprints + PsyArXiv. | preprint live |
| 6.4 Deposit dataset (CC-BY-4.0) to OSF. | data live |
| 6.5 Deposit posterior samples to OSF. | RDS files live |
| 6.6 Update Mel's `Moranetz/moranetz` profile README. | profile updated |
| 6.7 Insert LinkedIn posts #22 and #23 into queue. | posts queued |
| 6.8 Update auto-memory with Atlas-derived verified receipts. | memory updated |

---

## 7 · Repo file tree

```
closing-evidence-atlas/
├── README.md                          # Phase 5 — Persuasion-Max voice
├── EXECUTIVE_SUMMARY.md               # Phase 5
├── LIMITATIONS.md                     # Phase 5
├── PROTOCOL.md                        # ✅ this session
├── PLAN.md                            # ✅ this session
├── PROTOCOL_DEVIATIONS.md             # populated as deviations occur
├── LICENSE                            # MIT (code) — added Phase 6
├── LICENSE-DATA                       # CC-BY-4.0 (protocol/data) — added Phase 6
├── pyproject.toml                     # Phase 0 — added next session
├── renv.lock                          # Phase 3 — pinned R deps
├── .github/workflows/ci.yml           # Phase 0 — added next session
├── search/
│   ├── strategy.md                    # ✅ this session
│   ├── inclusion_criteria.md          # ✅ this session
│   ├── extraction_form.md             # ✅ this session
│   ├── search_log.md                  # Phase 1
│   ├── calibration_kappa.md           # Phase 1
│   ├── screening_log.csv              # Phase 1
│   └── prisma_flow.md                 # Phase 1
├── taxonomy/
│   ├── techniques.md                  # ✅ this session
│   └── voss_mi_mapping.md             # Phase 2
├── data/
│   ├── .gitignore                     # Phase 0 — added next session
│   ├── extracted_studies.csv          # Phase 2 (gitignored until G2)
│   ├── standardized_effects.csv       # Phase 2
│   └── rob_assessments.csv            # Phase 2
├── analysis/
│   ├── statistical_plan.md            # ✅ this session
│   ├── 01_load_and_validate.R         # Phase 2
│   ├── 02_primary_meta_analysis.R     # Phase 3
│   ├── 03_multiverse.R                # Phase 4
│   ├── 04_bias_diagnostics.R          # Phase 4
│   ├── 05_sensitivity.R               # Phase 4
│   └── fits/                          # rds files (Phase 3+)
├── results/
│   ├── posterior_summaries.csv        # Phase 3
│   ├── multiverse_summaries.csv       # Phase 4
│   ├── pcurve_*.csv                   # Phase 4
│   ├── selection_*.csv                # Phase 4
│   ├── sensitivity_*.csv              # Phase 4
│   └── survivor_classification.csv    # Phase 4
├── figures/                           # Phase 3+
├── notebooks/                         # exploratory only
├── manuscript/                        # Phase 5
├── scripts/
│   ├── validate_extraction.py         # Phase 2
│   ├── make_atlas.sh                  # one-shot reproducibility (Phase 5)
│   └── preflight_check.sh             # mirrors coastal-compass pattern (Phase 6)
└── tests/                             # unit tests for analysis code
```

---

## 8 · Pre-public-shipping checklist (gate before `gh repo create --public`)

Mirrors Mel's iOS App Store pattern. Every box must be checked before Phase 6.

- [ ] All tests pass (`pytest`, `Rscript -e 'testthat::test_dir("tests")'`)
- [ ] All analysis scripts run end-to-end via `make atlas` from a fresh clone
- [ ] All notebooks execute top-to-bottom from a fresh kernel
- [ ] CI green on the last commit
- [ ] No `TODO`, `FIXME`, or `XXX` markers in tracked files
- [ ] Every numeric claim in README cites a results file
- [ ] PROTOCOL.md unchanged from Atlas-G0 lock-in (or all changes logged in PROTOCOL_DEVIATIONS.md)
- [ ] LICENSE files present and correct
- [ ] README rendered in Persuasion-Max voice — passes "could a competitor swap their name in" test
- [ ] LIMITATIONS.md present and specific
- [ ] Quickstart runs end-to-end in under 30 minutes on a fresh clone
- [ ] `data/extracted_studies.csv` not committed (deposited to OSF instead per CC-BY-4.0)
- [ ] Repo description set on GitHub
- [ ] Pinned to Mel's profile (after public)
- [ ] Profile README updated to reference it
- [ ] Preprint live on OSF + PsyArXiv

---

## 9 · Voice + README structure (Phase 5 draft outline)

1. **Hard premise** — Most sales-closing literature is folklore. 200+ techniques are taught with confidence; almost none have been audited. This repo audits.
2. **What it is** — pre-registered systematic review + Bayesian meta-analysis + multiverse robustness audit. Decomposes the literature into named primitives, then asks which survive.
3. **Why it's interesting** — N of M techniques cleared the credibility threshold. Y are selection-fragile under publication-bias adjustment. Z are popular but empirically untouched.
4. **At a glance** — counted receipts: techniques cataloged, studies screened, studies included, total participants pooled, survivors, multiverse decisions tested.
5. **The best entry points** — README → EXECUTIVE_SUMMARY → preprint → per-technique appendix → data + posteriors on OSF.
6. **Empirical spine** — 5 bullets of headline findings.
7. **What this is not** — explicit cuts: not a sales-training manual, not a productivity tool, not a closing-script generator, not a substitute for practice.
8. **Honest limitations** — corpus-era, language-skew, solo-author screening, taxonomy-overlap, English-only, anglosphere-skewed populations, publication-bias residual after adjustment.
9. **Running it** — quickstart + reproducibility note.

---

## 10 · Risk register (Atlas-specific)

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| Database returns yield far below estimate | Low–Medium | Search strategy is broad and uses 9 sources + hand-search. If yield < 500 unique records after dedup, expand to grey literature and add forward-citation depth. |
| Many techniques have <5 studies → can't meta-analyze | Medium–High | Pre-registered: techniques with <5 studies are reported descriptively in RQ-5 only. This is *itself* a finding ("most named techniques are empirically untested"). |
| Solo-author screener bias | Medium | Calibration set + LLM-assisted re-screen + transparent reporting in deviation log. |
| Effect sizes unrecoverable from old papers | Medium | Pre-registered handling: studies with unrecoverable effects are cataloged but excluded from quantitative pooling; reported in PRISMA. |
| Bayesian fits don't converge | Low | Sequential remediation: longer warmup → tighter adapt_delta → reparameterization. After 3 attempts, flagged as nonconvergent. |
| Mel's commercial COI raised at peer review | Low | Disclosed up front in PROTOCOL § 14. Independent re-analysis materials made available. |
| Publication-bias adjustment shrinks every survivor below practical significance | Medium | Reported transparently. *Itself* a major finding ("the field's claimed effects are mostly selection-driven"). |
| Atlas finishes without sufficient survivors to make Sparring Partner persona library work | Medium | Sparring uses both CWS and CWS-borderline + a "fragile-but-popular" tier explicitly labeled. |

---

## 11 · What Mel needs to do at Atlas-G0 (right now)

1. Read `PROTOCOL.md` (~ 30 minutes).
2. Confirm or revise: scope, primary RQs, hypotheses (just H1), eligibility criteria, taxonomy v0.1.
3. Sign off OR request changes.

If silent for 24+ hours: I post 24-hour notice in the next session and proceed.
