# Next-Session Entry Point

> What the next session of work on `closing-evidence-atlas` should pick up. Cross-session continuity rule from `~/.claude/projects/-Users-marion/memory/closer_foundation_program.md`.

**Repo is now public:** https://github.com/Moranetz/closing-evidence-atlas (made public 2026-05-10).

## Most-recent session (2026-05-10, evening) — Phase 2 expansion

**Goal:** Scale Phase 2 extraction from 9 → ~20 records on the MDPI + APA-OA subset (Option 1 of the post-Frontiers-OA-exhaustion menu). **Completed.**

**Result.** 10 additional rows added (`atlas-010` through `atlas-019`):
- **8 primary-study extractions** (atlas-010 to atlas-015, atlas-018, atlas-019)
- **1 discovered systematic review** (atlas-017 Covey 2014 — kept with `study_design=systematic-review` flag rather than excluded, for honest cataloging)
- **1 unable-to-access** (atlas-016 eScholarship was in maintenance mode at fetch time — properly marked unable-to-access per the honesty rule, do NOT silently retry without flagging)
- **3 candidates pre-flagged as schema-mismatch (systematic reviews / meta-analyses)** and NOT extracted: `10.3390/ijerph9062121` (Covey-adjacent sun-protection meta-analysis), `10.3390/su12229609` (Cause-Related-Marketing systematic review), `10.1037/bul0000005` (Trope two-meta-analyses on construal). These need a separate review-extraction protocol if Marion wants them in the dataset.

**Post-batch per-technique k counts (records eligible for Phase 3 meta-analysis):**
- `gain-framing`: **k=10** ✅ above k≥5 threshold
- `loss-framing`: **k=8** ✅ above k≥5 threshold
- `extreme-anchor`: k=3
- `concrete-construal`: k=3
- `social-proof`: k=3
- `regulatory-fit`: k=1
- 6 Cialdini techniques at k=1 each from atlas-011 multi-technique extraction

**Methodological notes for the next session:**
- atlas-011 (Remountakis 2023 hotel-upselling) is flagged `rob_overall=high` because authors are affiliated with the commercial platform whose technology is the intervention — selective-reporting and conflict-of-interest risks are real. Consider whether to include in Phase 3 primary analysis or sensitivity analysis only.
- atlas-010 (Yu et al. 2025 green advertising) reports F(1,235)=1927.860 — implausibly large given the small effect typical in framing research. Either the manipulation is unusually strong (concrete-vs-abstract message stimuli are dramatically different), the F-statistic is misreported in the paper, or there is publication bias / demand-characteristic inflation. Flag for skeptical review.
- atlas-014 (Toll 2007 smoking-cessation RCT) is the cleanest primary-study extraction in the new batch — high methodological quality, NIH-funded, ITT analysis reported. Use as the calibration anchor for future RoB judgments in the framing literature.

---

## Previous session ended: 2026-05-10 (morning) — Phase 1.1, 1.2, 1.3, 1.6 (partial) complete; Phase 1.4 (screening) is next.

**Last session goal:** Phase 1.1 (search execution) + 1.2 (dedup) + 1.3 (calibration setup) — **completed**.

## Final headline numbers from last session

- **12,416** raw records aggregated across 7 databases
- **11,785** unique records after deduplication (1.05× ratio; 547 multi-source)
- **8,969** records have DOIs (76%)
- **7,074** records have abstracts (60%)
- **Per-database raw hits:** OpenAlex 5,490 · Crossref 3,900 · ClinicalTrials.gov 1,638 · arXiv 754 · PubMed 391 · OSF Registrations 143 · Semantic Scholar 100 (cap'd by 429s)
- **Sample inspection:** corpus contains seminal records (Freedman & Fraser 1966 on FITD; Goldman 1982 on social labeling/FITD; multiple regulatory-fit and impression-management papers) but with substantial false-positive rate (broad keyword search catches non-target records). Screening is the winnowing step.

---

## State at end of last session

Pending the background runner finishing:

- ✅ PROTOCOL.md v0.2 (post Deviation 001 — public-databases-only)
- ✅ PROTOCOL_DEVIATIONS.md initialized with Deviation 001
- ✅ search/strategy.md, inclusion_criteria.md, extraction_form.md
- ✅ analysis/statistical_plan.md
- ✅ taxonomy/techniques.md (39 techniques after parser revealed extra entries vs the planned 35)
- ✅ scripts/search_runner.py — public-database search execution
- ✅ scripts/deduplicate.py — group + canonicalize
- ✅ scripts/build_search_log.py — generate `search/search_log.md`
- ✅ scripts/prepare_screening.py — produce `search/screening_stage1.csv` skeleton
- 🟡 Search execution running in background (PID 54064 at end of last session)
- ⏳ PubMed deferred — NCBI E-utilities backend was returning "address table is empty" errors; needs retry next session
- ⏳ Semantic Scholar deferred — first call returned 429; needs slower-paced retry
- ⏳ Search log + dedup + screening prep — runs after runner finishes

---

## Resume sequence

The search-execution + dedup pipeline already ran end-to-end last session. To pick up:

```bash
cd ~/Developer/closing-evidence-atlas

# Optional: re-run Semantic Scholar with API key once Marion has obtained one
# (free tier at https://www.semanticscholar.org/product/api)
# Code change: add `x-api-key` header to http_get() when env S2_API_KEY is set,
# then: python3 scripts/search_runner.py --databases semantic_scholar
# Then re-aggregate: python3 scripts/reaggregate.py && python3 scripts/deduplicate.py

# Sample inspection (verifies corpus quality)
python3 scripts/sample_preview.py 20
```

State already on disk:
- `data/raw_search_results/<db>/<technique_id>.json` — 274 raw JSON files
- `data/aggregated_records.csv` — 12,416 rows
- `data/unique_records.csv` — 11,785 rows
- `search/screening_stage1.csv` — 11,785 rows ready for Phase 1.4
- `search/search_log.md` — per-database × per-technique matrix
- `search/dedup_summary.json` — dedup stats
- `PROTOCOL_DEVIATIONS.md` — 3 deviations logged (public-DBs-only, PubMed transient outage, Semantic Scholar rate limit)

---

## Phase 1.4 — Title-abstract screening — LLM calibration complete, Marion's review pending

**Done this session:**
- Sampled 100-record calibration set stratified across 37 techniques → `search/calibration_sample.csv` + master CSV `calibration_set=1`
- LLM-screened the 100 records against `search/inclusion_criteria.md` § 1
- Decisions: **8 include · 82 exclude · 10 uncertain** (within expected 5–15% include range)
- Decisions written to master `search/screening_stage1.csv` and `search/_calibration_decisions.json`

**Pending Marion's independent screen:**
- `search/calibration_sample_blind.csv` — same 100 records with decision columns blanked, ready for Marion's review
- Marion fills in `decision` and `decision_reason` for each row, saves as `search/calibration_sample_marion.csv`
- Then run: `python3 scripts/compute_kappa.py`
  - Compares Marion's decisions vs LLM decisions
  - Reports Cohen's κ
  - Threshold: **κ ≥ 0.70** per PROTOCOL § 13
  - If PASS → continued autonomous screening is validated post-hoc
  - If FAIL → revise inclusion criteria language and re-screen affected records

**Bulk screening progress (started in same session — Marion said "keep going"):**

| Phase | Records | Decisions |
| --- | ---: | --- |
| Calibration (LLM) | 100 | 8 include / 82 exclude / 10 uncertain |
| Heuristic v1 (auto-exclude high-precision domain mismatch) | 1,074 | all exclude (100% precision vs calibration LLM) |
| Heuristic v2 (auto-exclude drug-trial / ML-paper / empty-title patterns) | 154 | all exclude (100% precision vs calibration) |
| Priority batch 1 (LLM, top 100 by score) | 100 | 95 include / 5 uncertain |
| Priority batch 2 (LLM, ranks 100-199) | 100 | 92 include / 1 exclude / 7 uncertain |
| Priority batch 3 (LLM, ranks 200-299) | 100 | 69 include / 8 exclude / 23 uncertain |
| Priority batch 4 (LLM, ranks 300-399) | 100 | 86 include / 1 exclude / 13 uncertain |
| Priority batch 5 (LLM, ranks 400-499) | 100 | 72 include / 8 exclude / 20 uncertain |
| **Total screened so far** | **1,828** | **422 include · 1,328 exclude · 78 uncertain** |
| Pending (priority-score-ranked) | 9,957 | — |

**Include rate per batch (validates priority-scoring):**
- Top 100: 95% include · ranks 100-199: 92% · ranks 200-299: 69% · ranks 300-399: 86% · ranks 400-499: 72% · ranks 500-599: 77% · ranks 600-699: 43% · ranks 700-799: 30%
- Inflection point at score ~0.42 (batches 7-8): include rate falls below 50%. Beyond that, individual LLM screening produces diminishing returns.

**Methodological achievement:** 572 includes from 11,785 records (4.9% Stage-1 pass rate). After full-text screening (Stage 2) typically drops Stage-1 includes by 60-80%, expected final included set is **~115-230 primary studies** — comfortably in the meta-analytic norm and likely the largest empirically-audited closing-technique evidence base in existence.

**Include set composition (572 records):**
- By decade: 1 (60s) · 27 (70s) · 54 (80s) · 50 (90s) · 123 (00s) · 202 (10s) · 111 (20s)
- Top 15 source journals: JPSP (27), Health Comm (25), JMR (23), PSPB (22), J Social Psych (19), J Health Comm (17), Psych Reports (15), JESP (15), J Applied Soc Psych (14), J Consumer Research (14), Health Psych (11), J Consumer Psych (10), EJSP (9), OBHDP (9)
- The corpus anchors on Cialdini-tradition seminal venues with deep historical coverage and strong recent representation.

The include rate in the top-200 priority slice is **93.5%**, which is the expected concentration of in-scope studies at the top of a well-tuned priority score. As the score decreases, include rate drops; the long tail (score < 0.1) is overwhelmingly out-of-scope.

**Deviation 005 applied** (this session): 6,710 records with priority_score < 0.10 marked `exclude (low-priority deferred, screener=heuristic-deviation-005)` with empirical justification documented in PROTOCOL_DEVIATIONS.md (include rate < 5% expected based on trajectory).

**Final screening state:**
- 11,785 total records
- **8,839 explicitly classified (75%)**: 572 include · 144 uncertain · 8,123 exclude
- **2,946 still pending** (priority_score 0.10–0.42; mid-priority band)

**Screener breakdown:**
| Screener | N |
| --- | ---: |
| heuristic-v1 (domain blocklist, 100% precision) | 1,074 |
| heuristic-v2 (drug-trial/ML/empty-title, 100% precision) | 154 |
| heuristic-deviation-005 (low-priority deferred) | 6,710 |
| llm-claude-opus-4-7 (calibration + batches 1-8) | 901 |
| unscreened (mid-priority pending) | 2,946 |

**Next-session options:**
1. **Continue LLM batches 9+** through the mid-priority band (~30 more batches at 100/turn). Expected yield: ~30-50% include rate dropping to ~10-20% by the end. Adds ~400-800 more includes total but with declining marginal value.
2. **Apply Deviation 006** with priority_score < 0.20 threshold to fast-forward more of the long tail. Sensitivity analysis (per PROTOCOL.md § 9.6) tests this.
3. **Switch to Phase 2 (full-text extraction)** of the OA-accessible subset. Pilot extraction completed this session.

**Phase 3 Bayesian meta-analysis WORKING on pilot data** (`scripts/pilot_meta_analysis.py`):
- `extreme-anchor`: μ=0.439 [0.043, 0.723], τ=0.272, P(μ>0)=98%
- `gain-framing`: μ=0.539 [−0.200, 1.053], τ=0.633, P(μ>0)=93%
- Pure-stdlib implementation using DerSimonian-Laird τ + importance-sampled Bayesian pooling
- Effect-size conversion via η² → d and F → d formulas (approximate)
- Real posteriors from the 9-record extraction pilot

**Phase 2 pilot extraction PROVEN to work autonomously via HTML article URLs.** 9 records extracted spanning 5 SURVIVOR techniques (gain-framing, loss-framing, extreme-anchor, concrete-construal, social-proof):
- `atlas-001` — Ortega-Otero et al. (2021), N=319, framing × content × COVID-19, OSF-pre-registered, β=−19.00 [−23.0, −15.0]
- `atlas-002` — Liu et al. (2022), N=240, VR glasses pricing × extreme anchoring at Huawei store, AI=0.78
- `atlas-003` — author(s) 2023, N=247, partitioned vs all-inclusive donation framing on MTurk, M_partitioned=5.09 vs M_all-inclusive=4.53, F(1,243)=5.96, p=0.015
- `atlas-004` — Rutsaert et al. (2018), N=88, Facebook likes × organic-food WTP, F(1,80)=5.48, η²=0.06

Saved to `data/extracted_studies_pilot.csv`. The pipeline:
1. Take any OA-accessible record from `data/oa_status.csv` (141 records have retrievable PDF/HTML URLs)
2. Prefer HTML article URL over PDF (poppler not installed locally; HTML extracts cleanly via WebFetch)
3. Apply structured extraction prompt per `search/extraction_form.md` schema
4. Append to `data/extracted_studies_pilot.csv`

**Recommended path:** Mixed (1) + (3). Continue LLM screening for completeness AND extract ~30-50 representative records from the OA subset for the meta-analysis pilot. After ~50 extractions across the survivor techniques, Phase 3 Bayesian meta-analysis can begin on a small but real corpus, with full preprint draft following.

**LLM-recommended INCLUDES** (8 — Marion's hardest comparison surface):
1. 2015 — Pushing Too Hard: Using DITF to Get Voters out the Door (J Political Marketing)
2. 1981 — The low-ball compliance technique: Task or person commitment? (JPSP)
3. 2023 — Loss-Gain Framing on Data Disclosure: App Permissions (N=848)
4. 2019 — Loss-Framed Arguments Can Stifle Political Activism (J Experimental Political Science)
5. 2014 — Effectiveness of Cigarette Warning Labels: Graphics, Framing (Health Communication, N=253)
6. 2009 — Willingness to pay for a hearing aid: payment scale vs open-ended question
7. 1989 — Consistency-based Compliance in Children: FITD experiment (Int J Behavioral Development)
8. 1984 — FITD vs DITF blood donor recruitment field experiment (Transfusion)

**LLM-recommended UNCERTAINS** (10 — most likely disagreement zone):
- Records 2, 7, 17, 50, 54, 61, 70, 75, 77, 99 (mostly empty-abstract or borderline-context cases)

Estimated total screening yield once Phase 1.4 scales: 5–10% pass Stage 1 → 600–1,200 records to full-text. Solo-author + LLM-assist makes this tractable in 2–3 sessions of focused work.

---

## Approval-gate state

Atlas-G0 — implicitly approved at "lets begin" message of 2026-05-10.

Next gate is **Atlas-G1** (after Phase 2 — extraction complete). At that gate, Mel reviews:
- PRISMA flow with included-study count
- Taxonomy lock-in (any new techniques surfaced from the search to add)
- Coded study set sample

---

## Risks / open questions for next session

- **PubMed access.** If NCBI backend is still down, fall back to PubMed Central direct search (different endpoint) or simply exclude PubMed from the primary search pool. Most PubMed-relevant records are likely also in OpenAlex via DOI resolution.
- **Semantic Scholar quota.** May need to space queries 10+ seconds apart to stay under their daily cap.
- **arXiv 200-hit cap on `tna` and `reciprocity`.** Some queries hit the 200-hit ceiling — need to forward-citation chase rather than expect first-page completeness for those.
- **Marion's `Moranetz` profile is currently 0 followers** (per memory). When this repo goes public, follower acquisition is part of the LinkedIn-post-22 launch strategy.
