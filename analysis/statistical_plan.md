# Statistical Analysis Plan

Pre-registered statistical analysis plan for the Closing Evidence Atlas. Companion to `PROTOCOL.md` § 9. Any modifications post Atlas-G0 sign-off go through the deviation log.

---

## 1 · Software stack

| Tool | Version | Use |
| --- | --- | --- |
| R | ≥ 4.4 | Primary statistical environment |
| `brms` | ≥ 2.21 | Bayesian random-effects meta-analysis |
| `cmdstanr` | ≥ 0.8 | Stan backend for `brms` |
| `metafor` | ≥ 4.6 | Frequentist sensitivity analyses, PET-PEESE |
| `bayesplot` | ≥ 1.11 | Posterior visualization |
| `tidyverse` | ≥ 2.0 | Data manipulation |
| `revtools` | ≥ 0.4 | Reference deduplication |
| `specr` | ≥ 1.0 | Specification-curve analysis |
| `weightr` | ≥ 2.0 | Three-parameter selection model |
| `dmetar` | ≥ 0.1 | p-curve analysis |
| Python | ≥ 3.11 | Auxiliary tooling, search-result wrangling |

All package versions pinned via `renv` (R) and `pyproject.toml` (Python). Random seed: `20260510`.

---

## 2 · Effect-size standardization

Per PROTOCOL § 7.3:
- Continuous outcomes → Hedges' *g* (Borenstein et al. 2009 Eq. 4.18).
- Binary outcomes → log-odds-ratio. Computed via `metafor::escalc(measure = "OR", to = "if0all")` for zero-cell handling.
- Risk ratios converted to log-OR for pooling but reported back-transformed.
- Pearson *r* → Fisher's *z* → standardized *g* via Borenstein et al. (2009) Ch. 7.

Standard errors propagated through transformations using delta-method approximations.

For each effect, we record:
- `es_standardized_value` — the standardized effect
- `es_standardized_se` — SE on the standardized effect

---

## 3 · Primary meta-analytic model

For each technique with ≥ 5 eligible studies:

```
y_i ~ Normal(theta_i, sigma_i)         # likelihood; sigma_i fixed at extracted SE
theta_i ~ Normal(mu, tau)              # study-level random effect
mu ~ Normal(0, 0.5)                    # weakly-informative prior on Hedges' g scale
tau ~ Half-Normal(0, 0.3)              # weakly-informative between-study SD prior
```

For binary-outcome techniques (log-OR scale):

```
mu ~ Normal(0, 0.7)                    # weakly-informative on log-OR scale
tau ~ Half-Normal(0, 0.5)
```

Implemented in `brms`:

```r
fit <- brm(
  es_standardized_value | se(es_standardized_se) ~ 1 + (1 | study_id),
  data = technique_df,
  prior = c(
    prior(normal(0, 0.5), class = "Intercept"),
    prior(normal(0, 0.3), class = "sd")
  ),
  family = gaussian(),
  chains = 4, iter = 4000, warmup = 2000, cores = 4,
  seed = 20260510,
  control = list(adapt_delta = 0.99)
)
```

### Estimands (per technique)

1. Posterior median of `mu` — population-average effect.
2. 95% credible interval (CrI) on `mu` — equal-tailed posterior interval.
3. 90% CrI for sensitivity reporting.
4. P(`mu` > 0) — posterior probability of any positive effect in the practitioner-claimed direction.
5. P(`mu` > 0.20) — posterior probability of *practically significant* effect.
6. Posterior median and 95% CrI on `tau` — between-study heterogeneity.
7. 95% prediction interval (Higgins, Thompson, Spiegelhalter 2009) — interval for a *new* study from the population.

### Convergence diagnostics

- All R-hat ≤ 1.01.
- Effective sample size (bulk and tail) ≥ 1000 per parameter.
- No divergent transitions (or divergent count ≤ 1% with adapt_delta increase to 0.999).
- Posterior predictive checks via `pp_check()` reported per technique.

A fit failing convergence is rerun with: longer warmup; tighter `adapt_delta`; reparameterization. A non-converging fit after 3 attempts is flagged as `nonconvergent` in the survivor list and excluded from primary inference.

---

## 4 · Moderator analyses (RQ-3)

For techniques with ≥ 10 studies, per-moderator meta-regression:

```r
fit_mod <- brm(
  es_standardized_value | se(es_standardized_se) ~ 1 + moderator + (1 | study_id),
  data = technique_df,
  prior = c(
    prior(normal(0, 0.5), class = "Intercept"),
    prior(normal(0, 0.3), class = "b"),
    prior(normal(0, 0.3), class = "sd")
  ),
  ...
)
```

Pre-specified moderators (run separately, not jointly, to avoid power issues):
- `sales_context` (B2B vs. B2C vs. mixed)
- `transaction_type` (transactional vs. consultative)
- `channel` (in-person / phone / digital)
- `country_region` (collapsed to NA / EU / Asia / LatAm / Africa / Oceania)
- `mean_age` (continuous, centered)
- `year_of_study` (continuous, centered on 2000)
- `time_horizon` (immediate vs. delayed)
- `pre_registered` (yes vs. no)

Each moderator analysis reports:
- Posterior median and 95% CrI for the moderator coefficient.
- Posterior probability of the coefficient being in the hypothesized direction (where applicable).

Multiple moderators are *not* combined into a joint model except in pre-registered exploratory analyses (flagged in deviation log).

---

## 5 · Publication-bias diagnostics (RQ-4)

### 5.1 Funnel plot
- Per technique with ≥ 10 studies.
- Plot effect size against standard error.
- Visual asymmetry assessed by author + a second reader.

### 5.2 Egger's regression test
- Standard implementation via `metafor::regtest()`.
- Reported with caveat that Egger's test has low power with < 20 studies.

### 5.3 p-curve analysis
- `dmetar::pcurve()` per technique with ≥ 10 studies.
- Reports evidential value (right-skew test), p-curve power, and p-curve effect estimate.

### 5.4 Three-parameter selection model
- `weightr::weightfunct()` adjusting for selection conditional on p < 0.025 / 0.05 / 0.10 thresholds.
- Reported alongside primary estimate as sensitivity.

### 5.5 PET-PEESE
- Standard PET (precision-effect-test) and PEESE (precision-effect-estimate-with-standard-error) corrections.
- Reported with adjusted effect estimate; if adjusted estimate is not practically significant, the technique is flagged **selection-fragile**.

### 5.6 Trim-and-fill
- Reported but not used as primary; literature now consensus that trim-and-fill assumptions are restrictive.

---

## 6 · Multiverse / specification-curve analysis (RQ-2 robustness)

For each technique with ≥ 5 studies, run analytical multiverse:

| Decision | Levels |
| --- | --- |
| Inclusion filter | `all-eligible` / `low-rob-only` / `pre-registered-only` |
| Effect-size estimator | `hedges-g` / `log-or-where-convertible` |
| Prior on `mu` | `Normal(0, 0.5)` (default) / `Normal(0, 1)` (flat) / `Normal(0, 0.1)` (skeptical) |
| Outlier handling | `none` / `studentized-residual-2` / `leave-one-out` |
| Heterogeneity prior | `Half-Normal(0, 0.3)` / `Half-Cauchy(0, 0.5)` / `Truncated-Normal(0, 0.5)` |
| Comparator restriction | `any` / `inactive-only` / `active-only` |

Cross-product = 3 × 2 × 3 × 3 × 3 × 3 = **486** specifications per technique.

For each specification we extract: posterior median, 95% CI lower, 95% CI upper.

Specification-curve plot shows median and 90% interval ordered by magnitude, with which decisions drive the variation highlighted via a "decision matrix" beneath the curve (per Simonsohn et al. 2020 Fig. 1).

### Multiverse survivor threshold

A technique survives the multiverse if **≥ 80% of specifications produce a posterior 95% CrI on `mu` that excludes zero in the practitioner-claimed direction**.

The threshold is pre-registered. Sensitivity to the threshold (60%, 70%, 90%) is reported alongside primary.

---

## 7 · Sensitivity analyses

Run per technique with ≥ 5 studies:

1. **Excluding high-RoB studies** — primary model re-fit on low/moderate-RoB only.
2. **Leave-one-out** — primary model re-fit dropping each study; report range of posterior medians.
3. **Post-2015 only** — restrict to studies published 2015+ (post replication-crisis era).
4. **Pre-registered only** — restrict to pre-registered studies.
5. **Direct conceptual replications** — restrict to studies that explicitly cite a prior study and replicate its design.
6. **Industry-funded vs. independent** — split by funding source.

Each sensitivity reported alongside the primary estimate. Substantive divergence (> 50% shrinkage in posterior median) is flagged.

---

## 8 · Survivor classification (RQ-1)

A technique is **credibility-weighted-survivor (CWS)** if it satisfies all of:

| Criterion | Threshold |
| --- | --- |
| C1 — Sufficient evidence base | ≥ 5 eligible primary studies |
| C2 — Posterior interval excludes null | 95% CrI on `mu` excludes 0 in practitioner-claimed direction |
| C3 — Multiverse robustness | ≥ 80% of specifications produce CrI excluding 0 |
| C4 — Practical significance under PET-PEESE | adjusted |posterior median| ≥ 0.20 (Hedges' g) or ≥ 0.20 (log-OR) |
| C5 — Independence from commercial interest | not solely driven by industry-funded studies (sensitivity § 7.6) |

Classification:
- **CWS** — all 5 criteria satisfied
- **CWS-borderline** — 4 of 5 satisfied, with the unsatisfied criterion explicitly named
- **No CWS** — fewer than 4 satisfied

---

## 9 · Network meta-analysis (exploratory only)

If sufficient studies pair-wise compare techniques, an exploratory Bayesian network meta-analysis estimates ranking probabilities (SUCRA values) per technique. This is **not** the primary analysis and is flagged as exploratory throughout. Implementation via `multinma` package.

---

## 10 · Reporting

Each technique gets a one-page report comprising:
1. Forest plot of all included effects.
2. Posterior density of `mu`.
3. Funnel plot (if ≥ 10 studies).
4. Specification-curve plot.
5. Sensitivity analysis table.
6. Numeric summary: posterior median, 95% CrI, P(mu > 0), P(mu > 0.20), `tau`, prediction interval, classification.

Aggregated across techniques: ranked survivor list with credibility-weighted effect sizes; full descriptive landscape (RQ-5) showing what fraction of practitioner-named techniques have zero, < 5, or ≥ 5 eligible studies.

---

## 11 · Reproducibility

- All R / Python scripts version-controlled in `analysis/`.
- `make atlas` reproduces every figure and table from raw extracted data.
- `renv.lock` and `pyproject.toml` pin every dependency.
- A frozen Docker image will be built at Atlas-G3 to guarantee long-term reproducibility.
- Posterior samples (RDS files, ~ 200 MB total) released alongside the preprint via OSF.
