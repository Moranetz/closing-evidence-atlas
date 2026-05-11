# Closing-Technique Taxonomy v0.1

The pre-registered taxonomy of named sales-closing techniques to be audited in the Closing Evidence Atlas. This list is built from systematic reading of the practitioner literature. It is the **source of truth** for `technique_taxonomy_id` references in the extraction form.

**Status:** v0.1 draft. Pre-registered as part of Atlas-G0. Locked at Atlas-G1; post-G1 additions are explicit deviations logged in `PROTOCOL_DEVIATIONS.md`.

---

## Structure

Each technique entry includes:

- **`taxonomy_id`** — short canonical identifier (e.g., `fitd`).
- **Canonical name** — primary label.
- **Aliases** — alternative names used in the practitioner literature.
- **Practitioner source(s)** — books / programs naming the technique.
- **Practitioner-claimed mechanism** — why proponents claim it works.
- **Practitioner-claimed direction** — *positive on close rate* / *positive on contract value* / etc.
- **Cluster** — high-level family (compliance, framing, structural-close, social-cue, question-form, post-objection, negotiation-anchor).
- **Initial empirical-status guess** — `well-studied` / `partially-studied` / `untested-in-database`. *This is a prior, not a finding.*

Initial-status guesses are recorded for reflexivity; they do not influence inclusion or analysis.

---

## A · Compliance-gaining techniques

### `fitd` — Foot-in-the-door

- **Aliases:** FITD; gradual commitment; small-then-large request
- **Practitioner sources:** Cialdini (1984, 2021); Hopkins (1980); Sandler (1996); SPIN training materials
- **Mechanism (claimed):** small initial compliance creates self-perception of being a "compliant" person; subsequent larger request is harder to refuse without identity inconsistency.
- **Direction (claimed):** positive on compliance with a target request.
- **Cluster:** compliance
- **Empirical status (prior):** well-studied (Burger 1999 meta-analysis; Pascual & Guéguen 2005)

### `ditf` — Door-in-the-face

- **Aliases:** DITF; rejection-then-retreat; concession-after-extreme-request
- **Practitioner sources:** Cialdini (1984, 2021); Voss (2016) "extreme anchor"
- **Mechanism (claimed):** large initial request creates perception of concession when retreating to target; reciprocity norm activated.
- **Direction (claimed):** positive on compliance.
- **Cluster:** compliance
- **Empirical status (prior):** partially-studied (O'Keefe & Hale 1998 meta-analysis; replication concerns)

### `lowball` — Low-ball

- **Aliases:** lowball; bait-and-bump
- **Practitioner sources:** Cialdini (1984); car sales training literature.
- **Mechanism (claimed):** initial small commitment binds participant; raised price after commitment is harder to refuse than the same price offered initially.
- **Direction (claimed):** positive on compliance with the higher-priced offer.
- **Cluster:** compliance
- **Empirical status (prior):** partially-studied (Cialdini et al. 1978; Burger & Petty 1981)

### `tna` — That's-not-all

- **Aliases:** TNA; reciprocity-with-additions
- **Practitioner sources:** Cialdini (1984); infomercial / direct-response training literature.
- **Mechanism (claimed):** sequential added bonuses before counter-offer activates reciprocity and commits the buyer.
- **Direction (claimed):** positive on compliance.
- **Cluster:** compliance
- **Empirical status (prior):** partially-studied (Burger 1986; Pollock et al. 1998)

### `disrupt-then-reframe` — Disrupt-then-reframe

- **Aliases:** DTR; pattern interrupt
- **Practitioner sources:** Davis & Knowles (1999); NLP training literature.
- **Mechanism (claimed):** unexpected disruption creates micro-confusion; reframe in same breath bypasses critical evaluation.
- **Direction (claimed):** positive on compliance.
- **Cluster:** compliance
- **Empirical status (prior):** well-studied for original effect; replication concerns (Carpenter 2013)

---

## B · Cialdini's six principles (each tested separately)

### `reciprocity` — Reciprocity

- **Practitioner sources:** Cialdini (1984, 2021); Sandler (1996); SPIN.
- **Mechanism (claimed):** norm of reciprocation creates obligation following an unsolicited gift / favor / concession.
- **Direction:** positive on compliance, contract value.
- **Cluster:** social-cue
- **Empirical status (prior):** well-studied

### `scarcity` — Scarcity

- **Practitioner sources:** Cialdini (1984, 2021); e-commerce conversion-rate-optimization literature.
- **Mechanism (claimed):** loss-aversion + reactance: limited availability raises perceived value and urgency.
- **Direction:** positive on compliance, willingness-to-buy.
- **Cluster:** framing
- **Empirical status (prior):** well-studied

### `authority` — Authority cues

- **Practitioner sources:** Cialdini (1984, 2021); Challenger Sale.
- **Mechanism (claimed):** heuristic deference to expertise / status reduces deliberation cost.
- **Direction:** positive on compliance.
- **Cluster:** social-cue
- **Empirical status (prior):** partially-studied; central effect well-replicated, but commercial-context studies thinner.

### `social-proof` — Social proof

- **Practitioner sources:** Cialdini (1984, 2021); CRO / web design literature.
- **Mechanism (claimed):** uncertainty resolved by observing others' behavior; conformity heuristic.
- **Direction:** positive on conversion, willingness-to-buy.
- **Cluster:** social-cue
- **Empirical status (prior):** well-studied

### `liking` — Liking / similarity / rapport

- **Practitioner sources:** Cialdini (1984, 2021); Sandler; Voss.
- **Mechanism (claimed):** affect transfer from liked source to evaluated offer; similarity activates in-group cooperative heuristics.
- **Direction:** positive on compliance, trust.
- **Cluster:** social-cue
- **Empirical status (prior):** partially-studied

### `commitment-consistency` — Commitment & consistency

- **Practitioner sources:** Cialdini (1984, 2021); SPIN (linkage questions); Sandler.
- **Mechanism (claimed):** prior public stance creates pressure to act consistently.
- **Direction:** positive on compliance, deal close.
- **Cluster:** compliance
- **Empirical status (prior):** partially-studied

---

## C · Framing techniques

### `loss-framing` — Loss-aversion framing

- **Aliases:** loss frame; threat appeal (Cialdini); cost-of-inaction (Challenger).
- **Practitioner sources:** Tversky & Kahneman (1981); Dixon & Adamson (2011); Cialdini (2021).
- **Mechanism (claimed):** asymmetric weighting of losses vs. gains; status-quo bias activated.
- **Direction:** positive on close, urgency.
- **Cluster:** framing
- **Empirical status (prior):** well-studied (broad framing literature)

### `gain-framing` — Gain framing

- **Practitioner sources:** Hopkins; Tracy; SPIN.
- **Cluster:** framing
- **Empirical status (prior):** partially-studied; effect heterogeneous by domain.

### `regulatory-fit` — Regulatory fit

- **Aliases:** prevention-vs-promotion fit
- **Practitioner sources:** Higgins (1997, 1998); commercial application papers.
- **Mechanism (claimed):** matching the buyer's regulatory focus (prevention / promotion) to the message frame increases fluency and persuasion.
- **Direction:** positive on compliance.
- **Cluster:** framing
- **Empirical status (prior):** well-studied

### `concrete-construal` — Concrete-vs-abstract framing

- **Aliases:** psychological distance; CLT-aligned message
- **Practitioner sources:** Trope & Liberman (2010); Voss (2016, "calibrated specifics").
- **Mechanism (claimed):** psychologically near framing matches near construal of immediate decisions.
- **Direction:** positive on immediate close.
- **Cluster:** framing
- **Empirical status (prior):** well-studied

---

## D · Structural close techniques (named close-types from sales training)

### `assumptive` — Assumptive close

- **Aliases:** "shall we go with the standard package?"
- **Practitioner sources:** Hopkins (1980); Tracy (1995); Belfort training materials.
- **Mechanism (claimed):** default-option psychology; reframes the decision from "if" to "which".
- **Direction:** positive on close rate.
- **Cluster:** structural-close
- **Empirical status (prior):** untested-in-database (best guess; verification at Phase 1)

### `alternative-choice` — Alternative-choice close

- **Aliases:** "Tuesday or Thursday?"; either-or close
- **Practitioner sources:** Hopkins; Tracy; SPIN.
- **Mechanism (claimed):** narrows decision space; default option reduces overwhelm.
- **Direction:** positive on close.
- **Cluster:** structural-close
- **Empirical status (prior):** untested-in-database

### `summary-close` — Summary close

- **Aliases:** value-summary; wrap-up close
- **Practitioner sources:** Hopkins; Rackham (SPIN); Dixon (Challenger).
- **Mechanism (claimed):** explicit summary of agreed value reduces decision uncertainty.
- **Direction:** positive on close.
- **Cluster:** structural-close
- **Empirical status (prior):** partially-studied (SPIN summary-of-need-payoff line evidence)

### `trial-close` — Trial close

- **Aliases:** mini-close; commitment check
- **Practitioner sources:** Hopkins; Tracy; SPIN.
- **Mechanism (claimed):** elicits intermediate commitment; surfaces objections early.
- **Direction:** positive on close.
- **Cluster:** structural-close
- **Empirical status (prior):** partially-studied

### `takeaway` — Takeaway close

- **Aliases:** scarcity-close; pull-back; refusal-then-pursuit
- **Practitioner sources:** Voss (2016); Belfort; Cialdini (scarcity).
- **Mechanism (claimed):** activates reactance and loss aversion; creates pursuit dynamic.
- **Direction:** positive on close (counterintuitive).
- **Cluster:** structural-close
- **Empirical status (prior):** untested-in-database under this label; scarcity-overlap evidence exists.

### `ben-franklin` — Ben Franklin / pros-and-cons close

- **Aliases:** balance sheet close
- **Practitioner sources:** Hopkins; Tracy.
- **Mechanism (claimed):** systematic enumeration favors the seller's framing (more pros pre-loaded).
- **Direction:** positive on close.
- **Cluster:** structural-close
- **Empirical status (prior):** untested-in-database

### `puppy-dog` — Puppy-dog close

- **Aliases:** trial use; risk-reversal
- **Practitioner sources:** Hopkins; SaaS / e-commerce industry.
- **Mechanism (claimed):** endowment effect after possession.
- **Direction:** positive on close at trial-end.
- **Cluster:** structural-close
- **Empirical status (prior):** partially-studied (endowment literature)

### `sharp-angle` — Sharp-angle close

- **Aliases:** turnaround; if-I-can-then-will-you
- **Practitioner sources:** Hopkins; Belfort.
- **Mechanism (claimed):** locks objection into commitment via conditional concession.
- **Direction:** positive on close.
- **Cluster:** structural-close
- **Empirical status (prior):** untested-in-database

---

## E · Question-form techniques

### `calibrated-question` — Calibrated question

- **Aliases:** open-ended question; how-question
- **Practitioner sources:** Voss (2016); MI literature (Miller & Rollnick 2012); SPIN.
- **Mechanism (claimed):** elicits buyer-generated rationale; converts "no" to a problem-solving stance.
- **Direction:** positive on rapport, compliance, deal velocity.
- **Cluster:** question-form
- **Empirical status (prior):** well-studied (MI/OARS literature: 1500+ RCTs).

### `labeling` — Affect labeling

- **Aliases:** emotional labeling; reflection (MI)
- **Practitioner sources:** Voss (2016); Lieberman (2007); MI.
- **Mechanism (claimed):** verbalizing emotion reduces amygdala activation; signals empathy.
- **Direction:** positive on rapport, compliance.
- **Cluster:** question-form
- **Empirical status (prior):** well-studied (Lieberman 2007 fMRI + replications)

### `mirroring` — Mirroring (verbal repetition)

- **Practitioner sources:** Voss (2016); rapport literature.
- **Mechanism (claimed):** signals attention; elicits elaboration.
- **Direction:** positive on rapport, compliance.
- **Cluster:** question-form
- **Empirical status (prior):** partially-studied

### `accusation-audit` — Accusation audit

- **Practitioner sources:** Voss (2016).
- **Mechanism (claimed):** preemptively naming buyer's likely objections inoculates against them.
- **Direction:** positive on close.
- **Cluster:** question-form
- **Empirical status (prior):** untested-in-database

### `spin-implication` — SPIN implication question

- **Practitioner sources:** Rackham (1988).
- **Mechanism (claimed):** elicits buyer-generated cost of the problem; raises perceived problem severity.
- **Direction:** positive on close, contract value.
- **Cluster:** question-form
- **Empirical status (prior):** partially-studied (Rackham's IBM data; minimal replication)

### `spin-need-payoff` — SPIN need-payoff question

- **Practitioner sources:** Rackham (1988).
- **Mechanism (claimed):** elicits buyer-generated benefits; pre-commits buyer to solution rationale.
- **Direction:** positive on close.
- **Cluster:** question-form
- **Empirical status (prior):** partially-studied

---

## F · Negotiation-anchor techniques

### `extreme-anchor` — Extreme anchor

- **Aliases:** anchoring; high-anchor opening
- **Practitioner sources:** Tversky & Kahneman; Voss; Galinsky.
- **Mechanism (claimed):** initial number anchors counterparty's adjustment.
- **Direction:** positive on contract value.
- **Cluster:** negotiation-anchor
- **Empirical status (prior):** well-studied

### `precise-anchor` — Precise number anchor

- **Practitioner sources:** Galinsky; Mason et al. (2013).
- **Mechanism (claimed):** precise numbers signal information; counterparty adjusts less.
- **Direction:** positive on contract value.
- **Cluster:** negotiation-anchor
- **Empirical status (prior):** well-studied (Mason et al. 2013)

### `anchor-with-range` — Range anchor

- **Practitioner sources:** Ames & Mason (2015).
- **Mechanism (claimed):** range anchors with backed-bottom outperform point anchors.
- **Direction:** positive on contract value.
- **Cluster:** negotiation-anchor
- **Empirical status (prior):** partially-studied

### `bracketing` — Bracketing

- **Practitioner sources:** Voss (2016).
- **Mechanism (claimed):** offers a range that brackets the target; counterparty meets in the middle.
- **Direction:** positive on contract value.
- **Cluster:** negotiation-anchor
- **Empirical status (prior):** untested-in-database

---

## G · Post-objection techniques

### `feel-felt-found` — Feel-felt-found

- **Practitioner sources:** Hopkins; Tracy.
- **Mechanism (claimed):** validates concern, then social-proof reframes.
- **Direction:** positive on close after objection.
- **Cluster:** post-objection
- **Empirical status (prior):** untested-in-database

### `isolate-and-conquer` — Isolate-the-objection

- **Practitioner sources:** Sandler; Belfort.
- **Mechanism (claimed):** elicits commitment that this is the *only* objection; remove it and commitment follows.
- **Direction:** positive on close.
- **Cluster:** post-objection
- **Empirical status (prior):** untested-in-database

### `reverse-objection` — Boomerang / reverse objection

- **Practitioner sources:** Tracy.
- **Mechanism (claimed):** reframes objection as a reason to buy.
- **Direction:** positive on close.
- **Cluster:** post-objection
- **Empirical status (prior):** untested-in-database

---

## H · Closing-environment techniques

### `silence` — Strategic silence after offer

- **Aliases:** "first-to-speak loses"; tactical pause
- **Practitioner sources:** Sandler; Voss.
- **Mechanism (claimed):** discomfort-with-silence pushes counterparty to fill it (often with concession or commitment).
- **Direction:** positive on close.
- **Cluster:** closing-environment
- **Empirical status (prior):** untested-in-database

### `mutual-close-plan` — Mutual close plan

- **Aliases:** MAP (mutual action plan); MEDDIC paper-process.
- **Practitioner sources:** MEDDIC / MEDDPICC; Force Management.
- **Mechanism (claimed):** explicit shared timeline reduces stalls; multi-threading via named stakeholders.
- **Direction:** positive on close, deal velocity.
- **Cluster:** closing-environment
- **Empirical status (prior):** untested-in-database under this label; commercial-data evidence (Gong / SBI) exists but not academic.

### `multi-threading` — Multi-threading / champion-development

- **Practitioner sources:** Challenger Sale; MEDDIC; Sandler.
- **Mechanism (claimed):** parallel relationships across stakeholders prevents single-point-of-failure on close.
- **Direction:** positive on close in B2B.
- **Cluster:** closing-environment
- **Empirical status (prior):** untested-in-database

---

## Summary: pre-registered taxonomy size

- **Total cataloged techniques (v0.1):** 35
- **Cluster distribution:**
  - Compliance: 5
  - Cialdini six principles (each separate): 6
  - Framing: 4
  - Structural close: 8
  - Question-form: 6
  - Negotiation-anchor: 4
  - Post-objection: 3
  - Closing-environment: 3 (silence + 2 structural)
- **Initial empirical-status distribution:**
  - well-studied: 11
  - partially-studied: 11
  - untested-in-database: 13

These are pre-registered counts. They will be updated only via the deviation log if Phase 1 surfaces additional named techniques (anticipated; flagged at G1).

---

## Versioning

- v0.1 — initial taxonomy compiled from practitioner literature. Atlas-G0 candidate.
- v1.0 — Atlas-G1 lock-in (after Phase 1 search may add new techniques surfaced in literature).
- All subsequent changes via deviation log.
