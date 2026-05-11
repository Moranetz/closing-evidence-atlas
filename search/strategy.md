# Search Strategy

This document specifies the systematic-review search strategy for the Closing Evidence Atlas. Pre-registered as part of `PROTOCOL.md`. Any modification post Atlas-G0 sign-off is logged in `PROTOCOL_DEVIATIONS.md`.

---

## 1 · Search concept structure

The search uses the boolean structure:

```
( CLOSING-TECHNIQUE TERMS ) AND ( SALES / COMMERCIAL CONTEXT TERMS ) AND ( OUTCOME TERMS ) AND ( STUDY-DESIGN TERMS )
```

Each block defined below.

---

## 2 · Block A — Closing-technique terms

**Generic:**
- "closing technique*" OR "sales close" OR "sales closing" OR "close rate"
- "compliance technique*" OR "compliance gaining"
- "persuasion technique*" OR "persuasive appeal*"
- "influence tactic*" OR "social influence"
- "buying decision*" OR "purchase decision*"

**Named techniques (will be exhaustively listed; sample shown):**
- "foot in the door" OR "foot-in-the-door" OR "FITD"
- "door in the face" OR "door-in-the-face" OR "DITF"
- "low-ball" OR "lowball" OR "low ball"
- "that's not all" OR "that's-not-all" OR "TNA"
- "bait and switch" OR "bait-and-switch"
- "scarcity appeal*" OR "scarcity claim*"
- "social proof"
- "reciprocity" AND ("sales" OR "compliance" OR "persuasion")
- "authority cue*" OR "expertise cue*"
- "liking" AND "compliance"
- "anchoring" AND ("sales" OR "negotiat*" OR "price")
- "framing" AND ("gain" OR "loss") AND ("sales" OR "purchas*")
- "trial close*"
- "assumptive close*"
- "alternative close*"
- "summary close*"
- "takeaway" AND ("sales" OR "compliance" OR "persuasion")
- "calibrated question*"
- "labeling" AND ("compliance" OR "negotiation" OR "rapport")
- "mirroring" AND ("rapport" OR "sales" OR "compliance")

The full list is built from the cataloged taxonomy in `taxonomy/techniques.md`. Each named technique generates an own search-string variant.

---

## 3 · Block B — Sales / commercial context

- "sales" OR "salesperson*" OR "sales representative" OR "sales call" OR "sales pitch"
- "buyer*" OR "customer*" OR "consumer*" OR "client*"
- "marketing" OR "advertising" OR "negotiation"
- "purchas*" OR "buying" OR "transaction*" OR "commerce"
- "B2B" OR "B2C" OR "business-to-business" OR "business-to-consumer"
- "retail*" OR "e-commerce" OR "ecommerce"
- "telesale*" OR "cold call*" OR "outbound" OR "field sales"

---

## 4 · Block C — Outcome terms

- "compliance" OR "comply"
- "purchase intention*" OR "buying intention*" OR "intention to buy"
- "conversion*" OR "close rate" OR "win rate"
- "sales performance" OR "sales effectiveness"
- "willingness to buy" OR "willingness to pay"
- "deal" AND ("close*" OR "won" OR "lost")
- "decision" AND ("commit*" OR "yes" OR "agreement")

---

## 5 · Block D — Study-design terms

- "randomi?ed" OR "RCT" OR "randomi?ed controlled trial"
- "experiment*" OR "lab experiment*" OR "field experiment*"
- "A/B test*" OR "A-B test*" OR "split test*"
- "quasi-experiment*"
- "intervention" AND ("randomi?ed" OR "controlled")

---

## 6 · Database-specific implementations

### 6.1 PubMed (NLM)

```
((("closing technique"[tiab] OR "sales close*"[tiab] OR "compliance technique*"[tiab] OR "persuasion technique*"[tiab] OR "foot in the door"[tiab] OR "door in the face"[tiab] OR "low-ball"[tiab] OR "that's not all"[tiab] OR "scarcity"[tiab] OR "social proof"[tiab] OR "reciprocity"[tiab] OR "anchoring"[tiab] OR "framing"[tiab] OR "trial close*"[tiab] OR "assumptive close*"[tiab]))
AND
(("sales"[tiab] OR "salesperson*"[tiab] OR "buyer*"[tiab] OR "customer*"[tiab] OR "consumer*"[tiab] OR "purchas*"[tiab] OR "buying"[tiab] OR "negotiat*"[tiab] OR "B2B"[tiab] OR "retail*"[tiab]))
AND
(("compliance"[tiab] OR "purchase intention*"[tiab] OR "conversion*"[tiab] OR "close rate"[tiab] OR "willingness to buy"[tiab] OR "willingness to pay"[tiab]))
AND
(("randomi*"[tiab] OR "RCT"[tiab] OR "experiment*"[tiab] OR "field experiment*"[tiab] OR "A/B test*"[tiab] OR "intervention*"[tiab] OR "quasi-experiment*"[tiab]))
)
```

Date filter: 1970/01/01 to current.

### 6.2 PsycInfo (APA)

PsycInfo MeSH-style descriptors used in addition to free text:
- DE "Persuasive Communication" OR DE "Compliance" OR DE "Social Influences"
- DE "Marketing" OR DE "Consumer Behavior" OR DE "Sales Personnel"
- DE "Experimental Design" OR DE "Random Sampling"

Combined with the above free-text blocks. Full-text search restricted to peer-reviewed, English-language, 1970-current.

### 6.3 Scopus

```
TITLE-ABS-KEY(
("closing technique" OR "sales close*" OR "compliance technique*" OR "persuasion technique*" OR "foot in the door" OR "door in the face" OR ... )
AND
("sales" OR "salesperson*" OR "buyer*" OR "customer*" OR ... )
AND
("compliance" OR "purchase intention*" OR "conversion*" OR ... )
AND
("randomi*" OR "RCT" OR "experiment*" OR "field experiment*" OR ...)
)
AND PUBYEAR > 1969
AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"cp" ) )
AND ( LIMIT-TO ( LANGUAGE,"English" ) )
```

### 6.4 Web of Science (SSCI)

```
TS=( ("closing technique" OR ...) AND ("sales" OR ...) AND ("compliance" OR ...) AND ("randomi*" OR ...) )
Refined by: DOCUMENT TYPES = ( ARTICLE OR PROCEEDINGS PAPER )
            LANGUAGES = ( ENGLISH )
            Timespan = 1970-CURRENT
```

### 6.5 ABI/INFORM Complete and EBSCO Business Source Complete

Adapted to platform-specific syntax. Same conceptual blocks; full strings recorded in `search/search_log.md` after execution.

### 6.6 Google Scholar

- For citation chasing only.
- Top 200 hits per technique-specific query (e.g., "foot-in-the-door" "compliance" "experiment").
- Hits beyond 200 will not be reviewed unless flagged by forward-citation chasing.
- Limitations of Google Scholar acknowledged (no boolean parity with academic databases; ranking algorithm changes); Scholar is supplementary, not primary.

### 6.7 ProQuest Dissertations and Theses Global

Same conceptual blocks. Dissertations and theses, 1970-current, English.

### 6.8 Pre-registration registries

- AEA RCT Registry — manual review of every persuasion / compliance / sales-tagged registration.
- OSF Registries — search by keyword for our techniques.
- ClinicalTrials.gov — limited eligibility (most clinical), but MI-based persuasion trials in clinical settings will be reviewed for technique-mechanism overlap with sales closes.

---

## 7 · Hand-search

### 7.1 Forward and backward citation chasing
For every included study after Stage 2 screening:
- Backward: every cited reference checked against eligibility criteria.
- Forward: every paper that cites the included study (via Web of Science / Scopus / Google Scholar) checked.

This continues iteratively until no new eligible studies are identified through one full citation-chasing pass.

### 7.2 Top-journal hand-search

Last 10 years of tables of contents searched manually:
- *Journal of Marketing*
- *Journal of Marketing Research*
- *Journal of Consumer Research*
- *Marketing Science*
- *Journal of Personal Selling & Sales Management*
- *Industrial Marketing Management*
- *Journal of Consumer Psychology*
- *Journal of the Academy of Marketing Science*
- *Organizational Behavior and Human Decision Processes*
- *Journal of Applied Psychology*
- *Personality and Social Psychology Bulletin*
- *Journal of Personality and Social Psychology*

### 7.3 Prior reviews
Reference lists of:
- Schwepker (2003) — sales ethics review.
- Roman & Iacobucci (2010) — sales effectiveness meta.
- Sherer (2013) — telesales effectiveness review.
- Kennedy & Nieuwerburgh (2013) — sales training meta.
- Cialdini & Goldstein (2004) — social influence review.
- Alaybek et al. (2022) — sales personality meta.

---

## 8 · Deduplication and management

- Records exported to RIS / CSV per database.
- Imported into a Zotero collection (`closing-evidence-atlas-master`).
- Deduplicated using the `revtools` R package (Westgate 2019), then manual second-pass deduplication.
- Final unique-record set shipped to the screening tool (Rayyan or equivalent).
- All databases timestamped at search execution; full hit counts recorded in `search/search_log.md`.

---

## 9 · Search log

The search log will record per database:
- Date of execution
- Full search string (verbatim)
- Total hit count
- Hits exported
- Notes on platform-specific peculiarities

`search/search_log.md` is created at Phase 1 execution and committed to git.

---

## 10 · Estimated yield

Based on prior reviews in adjacent areas:
- Total returned records (before dedup): estimated 8,000–15,000.
- Unique records after dedup: estimated 5,000–9,000.
- Title-abstract screen pass rate: estimated 5–10% → 250–900 records to full-text screen.
- Full-text pass rate: estimated 20–40% → 50–360 included studies.

These are pre-registered estimates. Actual yield will be reported in PRISMA flow.

---

## 11 · Updates

If the search execution date is more than 12 months before final preprint release, the search will be re-run with the same strategy and any newly identified eligible studies added. This pre-empts the "search-recency" critique commonly raised at peer review.
