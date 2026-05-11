# Inclusion / Exclusion Criteria

Operational decision rules for the title-abstract screen and full-text screen of the Closing Evidence Atlas. Pre-registered as part of `PROTOCOL.md` § 4.

These are the rules screeners apply per record. Borderline cases are flagged for consensus; default is *include* at title-abstract stage and *exclude* at full-text stage if the borderline is unresolved (conservative full-text screen).

---

## 1 · Title-abstract screen (Stage 1)

Include the record at Stage 1 if **all of the following are plausibly true** based on the title and abstract:

| Criterion | Plausibly true means |
| --- | --- |
| **Population** | Participants are buyers, customers, consumers, or experimental analogs in a commercial / persuasion-relevant decision setting. |
| **Intervention** | The study describes manipulation of a closing-relevant technique (named or describable). |
| **Outcome** | The study reports at least one eligible primary outcome (close rate, conversion, compliance, contract value, cycle time) or eligible secondary outcome. |
| **Design** | The study uses random assignment, quasi-random assignment, or a credible identification strategy. |
| **Time** | Published 1970 or later. |
| **Language** | English. |
| **Type** | Peer-reviewed article, peer-reviewed conference paper, dissertation, or registered protocol with results. |

Exclude at Stage 1 if **any** of the following are true:

- Title clearly identifies the paper as a theoretical / conceptual review with no empirical contribution.
- Title clearly identifies the paper as a single-case study, anecdote, or autobiographical account.
- Abstract describes a knowledge-test outcome (sales-training measure of knowledge gained) without a behavioral outcome.
- Setting is purely intra-organizational (peer-to-peer with no commercial decision).
- Setting is purely clinical / therapeutic (medical adherence) **and** the paper does not draw a sales-mechanism parallel.

---

## 2 · Full-text screen (Stage 2)

Include the study at Stage 2 if **all of the following are confirmed** in the full text:

### 2.1 Population
- Real or experimental participants in a commercial decision-making role (buyer, consumer, customer, lab participant in a buying simulation, field experiment subject).
- N ≥ 30 (sample-size minimum to ensure reasonable statistical signal).
- Adult participants (≥ 18 years; or developmentally relevant population in a buying simulation).

### 2.2 Intervention
- The manipulation operationalizes one or more named techniques in our taxonomy (`taxonomy/techniques.md`).
- The operationalization is described with sufficient detail to map unambiguously to a single named technique. (Borderline → include but flag for taxonomy review.)
- The manipulation is reproducible from the paper's description (or supplemental materials).

### 2.3 Comparator
- Active comparator (alternative technique) **or** inactive comparator (no-pitch / generic-pitch baseline) **or** within-subject baseline.
- Single-arm with no comparator → **exclude**.

### 2.4 Outcome
- At least one eligible primary outcome (§4.4 of PROTOCOL.md): close rate, conversion, compliance, contract value, cycle time.
- Effect size or sufficient summary statistics for effect-size reconstruction.
- Outcome measured at least at the per-decision / per-transaction level. Aggregate-only quarterly outcomes (e.g., regional sales totals) are excluded for inability to map to technique-level effect.

### 2.5 Design
- Random assignment **or** quasi-random with credible identification (instrumental variable, regression discontinuity, difference-in-differences with parallel-trends evidence, propensity-score matching with explicit balance check).
- Pre-post designs without a control group → **exclude**.
- Cross-sectional correlational analysis without identification → **exclude**.
- Mixed-method studies are eligible if the quantitative component independently meets the criteria.

### 2.6 Reporting quality
- Sufficient information to compute or extract effect size.
- Sample size per arm reported.
- Outcome operationalization described.

### 2.7 Setting
- Real-world commercial setting **or** experimental simulation of a commercial decision.
- Lab studies eligible **only if** the dependent variable is a behavioral analog of buying / compliance / agreement (not solely self-reported attitude or intention).

---

## 3 · Calibration set procedure

Before main screening:
1. Random sample of **100 unique records** drawn from the deduped database.
2. Two independent screeners (M. Moranetz + secondary; see PROTOCOL § 13.1 for solo-author deviation) apply the criteria to all 100.
3. Per-record decisions compared.
4. Inter-rater agreement computed (Cohen's κ).
5. Target: κ ≥ 0.70.
6. If κ < 0.70: discrepancies discussed, criteria revised, calibration set re-run on a fresh 100 records.
7. Calibration outcome reported in PRISMA section.

---

## 4 · Disagreement resolution

### 4.1 Title-abstract stage
- Disagreement → escalate to full-text screen (conservative).
- No interim consensus call needed.

### 4.2 Full-text stage
- Disagreement → both screeners re-read the section in question.
- Discussion to consensus.
- If no consensus → flag for third-party adjudication (deferred decision; recorded in screening log).
- Solo-author deviation: third-party adjudication via LLM-assisted re-reading is permitted but explicitly logged and limited to ≤ 5% of full-text decisions.

---

## 5 · Special-case decision rules

### 5.1 Cialdini's six principles
Each of {reciprocity, scarcity, authority, social proof, liking, commitment-and-consistency} is a separate technique in our taxonomy. A study that manipulates "reciprocity" is included for the **reciprocity** technique only, even if it discusses other principles theoretically.

### 5.2 Dual / combined manipulations
Studies manipulating two or more named techniques simultaneously (e.g., scarcity × authority) are included for **each** technique, with a flag in the data extraction noting that the effect is jointly estimated. The interaction analysis is exploratory and noted in the deviation log if pursued.

### 5.3 Voss-rebranded techniques
Voss's "calibrated questions" map to MI's "open questions" (OARS). For coding purposes, a study testing one is coded as also testing the other unless the operationalization differs substantively. The mapping is documented in `taxonomy/voss_mi_mapping.md` (deferred to Phase 2).

### 5.4 Cultural / linguistic translations
A study run in a non-English-speaking population using a translated technique manipulation is eligible if the paper itself is published in English. The translation choice is recorded as a moderator candidate.

### 5.5 Online vs. offline analogs
A "scarcity countdown timer" on an e-commerce site and a "limited-time offer" in a retail setting are coded under the same technique (scarcity), with channel as a moderator. Splitting techniques by channel is reserved for sub-group analysis only.

---

## 6 · Excluded but cataloged

The following are systematically excluded from quantitative meta-analysis but cataloged for descriptive reporting (RQ-5):

- Studies with effect sizes unrecoverable from the published text.
- Studies with N < 30.
- Studies whose technique operationalization could not be unambiguously mapped to a single taxonomy entry.
- Pure qualitative studies of closing behavior.
- Theoretical / conceptual papers naming new techniques without empirical test.

These contribute to the "descriptive landscape" reporting per PROTOCOL § 12.

---

## 7 · Pilot of the criteria

This criteria document will be piloted on the calibration set (§3) before main screening. Any criterion that shows κ < 0.50 inter-rater agreement on its own will be revised before main screening proceeds.
