# Closing Evidence Atlas — for CROs and VPs of Sales

A 5-minute read. The full pre-registered systematic review is in this repo; the methodological apparatus and statistics live in `manuscript/atlas_v0.1.md`. This file is for the conversation, not the paper.

---

## The headline

**Of the 39 named sales-closing techniques the practitioner canon teaches, 15 — almost 40% — have zero peer-reviewed empirical studies meeting the inclusion criteria of a pre-registered systematic review.** Most of your team's sales training is built on these.

The 15 with no evidence include the most heavily marketed moves:

- The assumptive close
- The alternative-choice close
- The summary close
- The trial close
- The takeaway close
- The Ben Franklin close
- The sharp-angle close
- The puppy-dog close
- The mutual close plan
- Multi-threading
- The accusation audit
- SPIN's implication question
- SPIN's need-payoff question
- Mirroring (verbal repetition)
- Bracketing

This isn't a claim that these don't work. It's a claim that **the academic literature has not tested them** at the level a buyer with a quantitative background would expect — randomized or quasi-experimental design, peer review, replicated outcome measure.

## What does have evidence

The techniques with substantial peer-reviewed empirical support cluster in two areas:

**Compliance mechanics** — foot-in-the-door (FITD), door-in-the-face (DITF), low-ball, that's-not-all, regulatory fit. These have decades of randomized lab and field work. Pooled effect sizes in the audit's Phase 3 pilot:

- Gain-framing: pooled Cohen's d ≈ 0.35 (k=9 records) — consistent, replicable, mid-strength effect
- Loss-framing: d ≈ 0.33 (k=7) — similar; loss-framing isn't reliably stronger than gain-framing despite practitioner consensus
- Regulatory-fit: d ≈ 0.48 (k=3) — credible
- Commitment-consistency: d ≈ 0.59 (k=2) — credible, small sample
- Extreme-anchor: d ≈ 0.44 (k=2) — credible, small sample

**Social-cue mechanics** — reciprocity, social proof, authority, scarcity. These also have substantial literature, though the practitioner-version of "social proof" often goes beyond what the studies test.

## The two-literature gap

This is the finding worth bringing into a CRO conversation.

**Your sales team's training book emphasizes:** structural closes (assumptive, alternative-choice, summary, trial, takeaway, puppy-dog) and Voss-style negotiation moves (calibrated questions, accusation audits, mirroring, bracketing).

**The peer-reviewed academic literature has studied:** compliance and framing mechanisms (FITD, DITF, gain/loss framing, lowball, regulatory fit, social proof, reciprocity).

The two sets barely overlap. A practitioner reading the academic literature encounters a different set of named techniques than the practitioner canon emphasizes. An operator deploying the structural closes is deploying techniques with no peer-reviewed empirical foundation — **not necessarily ineffective, but unvalidated by the standard a thoughtful customer's CTO or CFO would apply.**

## What this means for your sales team's training

Three practical implications:

1. **Don't replace the practitioner canon wholesale.** Long-tenured AEs deploy the assumptive close, the takeaway close, the trial close because they get results in their experience. Practitioner know-how is real evidence even when academic literature is silent. The Atlas is not a permission slip to overrule field-tested moves.

2. **Stop training as if the practitioner canon is settled science.** The training-deck claim "research shows the assumptive close converts 23% better" is not supported. There is no published study testing the assumptive close at peer-reviewed inclusion standards. When your AEs are coached on these techniques, the framing should be "field-tested, mechanism-plausible" — not "research-backed."

3. **The techniques with real evidence are underused in training.** Gain/loss framing, regulatory fit, FITD, DITF, and commitment-consistency have substantial peer-reviewed support and are mid-strength effects (d ≈ 0.3-0.6). These are the moves where a hiring manager could honestly say "we train on this because the research supports it." Most sales-training programs underweight them.

## What this audit is — and is not

**What it is:** A pre-registered systematic review of the peer-reviewed empirical literature on named sales-closing techniques. PRISMA 2020 conformant. 11,785 records searched across 7 public databases. 572 included after Stage-1 screening. Full deviation log committed before any data inspection.

**What it is not:** A sales-training manual. A closing-script generator. A final survivor list (Phase 3 multiverse + bias-adjustment work is ongoing). A claim that the unstudied techniques are ineffective.

## Caveats worth surfacing in any conversation about this

- **Public-databases-only.** Scopus, Web of Science, PsycInfo, and EBSCO Business Source Complete were not searched. Coverage gap is estimated at 5-15% of historical marketing-journal records.
- **English-only.**
- **Solo-author with LLM-assisted screening.** Inter-rater κ validation is committed in the methodology but pending a second human rater's pass.

## How to read the rest

If you have 30 minutes:
- `README.md` — the project overview
- `results/stage1_survivor_report.md` — per-technique evidence-base summary
- `figures/forest_pilot.svg` — visual representation of the per-technique posteriors

If you have an afternoon:
- `manuscript/atlas_v0.1.md` — the full preprint draft
- `PROTOCOL.md` — the pre-registered methodology
- `PROTOCOL_DEVIATIONS.md` — every protocol change and the empirical justification

If you'd like to discuss any of the specific techniques or the methodology, or want this audit narrowed to a particular segment of your team's training — that's a conversation I'd welcome.

---

*Marion Moranetz · github.com/Moranetz/closing-evidence-atlas*
