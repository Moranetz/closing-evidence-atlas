# Data Extraction Form

This form is the structured instrument used to extract data from each included study. Pre-registered as part of `PROTOCOL.md` § 7.1.

The implementation is a CSV file (`data/extracted_studies.csv`, gitignored until Atlas-G2 sign-off) with one row per study × technique × outcome. A single study testing multiple techniques or outcomes generates multiple rows.

---

## 1 · Identification fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `study_id` | string | yes | Internal sequential ID (`atlas-001`, `atlas-002`, …) |
| `doi` | string | no | DOI if assigned |
| `authors` | string | yes | Last names, comma-separated |
| `year` | int | yes | Publication year |
| `title` | string | yes | Verbatim |
| `journal` | string | yes | Journal / proceedings / "dissertation" / "preprint" |
| `volume_issue_pages` | string | no | Where applicable |
| `record_source` | enum | yes | `pubmed`/`psycinfo`/`scopus`/`wos`/`abi-inform`/`ebsco`/`scholar`/`proquest`/`hand-search`/`citation-chase` |

---

## 2 · Study-design fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `study_design` | enum | yes | `rct`/`cluster-rct`/`field-experiment`/`lab-experiment`/`quasi-experiment-iv`/`quasi-experiment-rdd`/`quasi-experiment-did`/`quasi-experiment-psm` |
| `setting` | enum | yes | `field-real-sales`/`field-experimental-sales`/`lab-buying-sim`/`lab-compliance`/`online-experiment`/`telesales`/`retail-store`/`other` |
| `sales_context` | enum | yes | `b2b`/`b2c`/`mixed`/`charitable`/`unspecified` |
| `transaction_type` | enum | yes | `transactional`/`consultative`/`hybrid`/`unspecified` |
| `channel` | enum | yes | `in-person`/`phone`/`email`/`web`/`chat`/`mixed`/`unspecified` |
| `country` | string | yes | ISO 3166 country code |
| `language_of_intervention` | string | yes | ISO 639 language code |
| `pre_registered` | enum | yes | `yes-osf`/`yes-aea`/`yes-other`/`no`/`unclear` |
| `pre_registration_url` | string | no | URL if applicable |
| `funding_source` | string | yes | Verbatim from acknowledgments |
| `coi_disclosed` | enum | yes | `yes-none-declared`/`yes-disclosed`/`no-disclosure`/`unclear` |

---

## 3 · Sample fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `n_total` | int | yes | Total analyzable sample |
| `n_treatment` | int | yes | Treatment-arm sample (or N per condition for multi-arm) |
| `n_control` | int | yes | Control-arm sample |
| `n_arms` | int | yes | Number of independent arms |
| `mean_age` | float | no | Where reported |
| `pct_female` | float | no | Where reported |
| `participant_role` | enum | yes | `consumer`/`buyer-b2b`/`student`/`crowdworker`/`mixed`/`other` |
| `attrition_rate` | float | no | Reported attrition % |

---

## 4 · Intervention fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `technique_taxonomy_id` | string | yes | Foreign key to `taxonomy/techniques.md` |
| `technique_label_in_paper` | string | yes | The exact label the paper uses (may differ from taxonomy canonical) |
| `operationalization_verbatim` | string | yes | Quote from paper describing the manipulation (≤ 500 chars) |
| `dose_or_intensity` | string | no | E.g., "single foot-in-the-door request" vs. "two stacked FITD requests"; free text |
| `comparator_type` | enum | yes | `inactive`/`alternative-technique`/`within-subject-baseline`/`waitlist` |
| `comparator_description` | string | yes | What the control received |

---

## 5 · Outcome fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `outcome_id` | string | yes | Sequential within study (`atlas-001-out-1`, …) |
| `outcome_type` | enum | yes | `close-rate`/`conversion`/`compliance`/`contract-value`/`cycle-time`/`willingness-to-buy`/`willingness-to-pay`/`trust`/`rapport`/`behavioral-intention` |
| `outcome_measurement` | enum | yes | `binary`/`continuous`/`count`/`time` |
| `outcome_operationalization_verbatim` | string | yes | Quote describing the outcome measure |
| `time_horizon` | enum | yes | `immediate`/`same-session`/`same-day`/`<1-week`/`1-week-to-1-month`/`>1-month` |
| `n_outcome` | int | yes | N analyzed for this outcome |

---

## 6 · Effect-size fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `es_as_reported_value` | float | yes | The effect size as reported in the paper |
| `es_as_reported_metric` | enum | yes | `cohen-d`/`hedges-g`/`cohen-f`/`odds-ratio`/`log-odds-ratio`/`risk-ratio`/`risk-difference`/`pearson-r`/`mean-diff`/`raw-proportion-diff` |
| `es_as_reported_ci_lower` | float | no | If reported |
| `es_as_reported_ci_upper` | float | no | If reported |
| `es_as_reported_se` | float | no | If reported |
| `es_as_reported_p` | float | no | If reported |
| `es_standardized_value` | float | yes | Standardized to Hedges' *g* (continuous) or log-OR (binary) per PROTOCOL § 7.3 |
| `es_standardized_se` | float | yes | Standard error after standardization |
| `es_reconstruction_method` | enum | yes | `as-reported`/`from-t-and-df`/`from-F-and-df`/`from-chi-squared`/`from-2x2-table`/`from-means-and-sds`/`from-p-value`/`unrecoverable` |
| `es_direction_aligned_to_practitioner_claim` | enum | yes | `yes`/`no`/`unclear` |

---

## 7 · Risk-of-bias fields (Cochrane RoB 2.0 / ROBINS-I adapted)

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `rob_randomization` | enum | yes | `low`/`some-concerns`/`high`/`na` |
| `rob_deviations` | enum | yes | `low`/`some-concerns`/`high`/`na` |
| `rob_missing_outcome_data` | enum | yes | `low`/`some-concerns`/`high`/`na` |
| `rob_outcome_measurement` | enum | yes | `low`/`some-concerns`/`high`/`na` |
| `rob_selective_reporting` | enum | yes | `low`/`some-concerns`/`high`/`na` |
| `rob_overall` | enum | yes | `low`/`some-concerns`/`high` |
| `rob_notes` | string | no | Free text explaining marginal calls |

---

## 8 · Coder metadata

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `extracted_by` | string | yes | Coder identifier |
| `extraction_date` | date | yes | YYYY-MM-DD |
| `second_extractor` | string | no | If double-extracted |
| `agreement_status` | enum | yes | `single-extractor`/`double-agreement`/`double-disagreement-resolved`/`double-disagreement-unresolved` |
| `notes` | string | no | Free text |

---

## 9 · Validation rules

The CSV is validated programmatically (`scripts/validate_extraction.py` — to be written in Phase 2):
- Every required field must be non-empty.
- `n_treatment + n_control ≤ n_total + 0.05 * n_total` (slack for rounding / dropouts).
- `es_standardized_value` and `es_standardized_se` must both be present unless `es_reconstruction_method == unrecoverable`.
- `technique_taxonomy_id` must resolve to a valid entry in `taxonomy/techniques.md`.
- Studies marked `unrecoverable` flow to qualitative synthesis only; flagged in PRISMA accordingly.

---

## 10 · Pilot extraction

Before main extraction, **10 randomly selected eligible studies** are double-extracted using this form. Per-field agreement reported. Form revised if any field shows ≥ 30% disagreement before main extraction proceeds.
