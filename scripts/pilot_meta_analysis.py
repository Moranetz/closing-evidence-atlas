#!/usr/bin/env python3
"""
Phase 3 pilot — pure-stdlib Bayesian random-effects meta-analysis.

Implements a simplified version of PROTOCOL.md § 9.2 in Python so that real
posterior estimates can be produced on the pilot extraction without requiring
R + brms + cmdstanr installation. The full preprint analysis uses
analysis/02_primary_meta_analysis.R for protocol-conformant Stan-backed
inference; this Python implementation is for demonstration and rapid iteration.

Method:
  1. Per-technique with k >= 2 standardized effects + SEs
  2. tau estimated via DerSimonian-Laird (closed form, MoM)
  3. mu posterior sampled by Monte Carlo:
       Repeat M times: sample tau from a half-normal proposal,
       compute precision-weighted mean of yi given tau,
       output mu_draw ~ Normal(precision_weighted_mean, weighted_se)
  4. Posterior summary: median, 95% CrI, P(mu > 0)

This is NOT a Stan-quality MCMC sampler. It's a "rough Bayesian" reasonable
approximation suitable for pilot demonstration. The R/brms script is what
produces preprint-quality inference.

Stdlib only.
"""

from __future__ import annotations

import csv
import math
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PILOT_PATH = REPO / "data" / "extracted_studies_pilot.csv"
OUTPUT_PATH = REPO / "results" / "pilot_posterior_summaries.csv"

random.seed(20260510)

N_MONTE_CARLO = 10_000


def parse_pilot(path: Path) -> list[dict]:
    """Parse pilot CSV; convert reported effect sizes to approximate Cohen's d
    with associated SE. Skip records where conversion isn't tractable.
    """
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if "STAGE-2 EXCLUDE" in (r.get("rob_notes") or ""):
                continue
            for tid in (r.get("technique_taxonomy_id") or "").split(";"):
                tid = tid.strip()
                if not tid:
                    continue
                d, se = approximate_d(r)
                if d is None:
                    continue
                rows.append({
                    "study_id": r["study_id"],
                    "technique_taxonomy_id": tid,
                    "year": r.get("year", ""),
                    "n_total": r.get("n_total", ""),
                    "d_approx": d,
                    "se_approx": se,
                    "rob_overall": r.get("rob_overall", ""),
                    "pre_registered": r.get("pre_registered", ""),
                })
    return rows


def approximate_d(r: dict) -> tuple[float | None, float | None]:
    """Best-effort approximate Cohen's d + SE from various effect-size metrics.

    Conversion formulas (rough; full Phase 3 uses metafor::escalc):
      - η² (partial) → d ≈ 2*sqrt(η²/(1-η²))                 [Cohen 1988]
      - F(1, df_within) → η²_p = F / (F + df_within) → d
      - F-df1-df2 metric label (df encoded in metric) → η²_p → d
      - t-statistic + df → r → d  [Rosenthal 1991]
      - β-standardized + t-statistic + df → r → Fisher z → d
      - Unstandardized β (VAS scale) → too domain-specific, skip
      - Raw mean difference + SD → d = (M1 - M2) / SD_pooled
      - Adjusted-OR + CI → log-OR with SE from CI, then d = log-OR × sqrt(3)/π
      - Anchoring index → not standardizable; skip
    """
    metric = (r.get("effect_size_metric") or "").lower()
    val = (r.get("effect_size_value") or "").strip()
    n_total_raw = (r.get("n_total") or "").strip()
    n = int(n_total_raw) if n_total_raw.isdigit() else None
    if not val or not n:
        return None, None

    # Try to extract a number
    try:
        v = float(val.split()[0].replace(",", ""))
    except (ValueError, IndexError):
        v = None

    if "eta-squared" in metric or "eta-partial-squared" in metric:
        # Use whichever eta-squared appears in the value field.
        # Methodological note: if the value field has multiple 0.XX-form
        # numbers, prefer the FIRST one (the primary reported value) rather
        # than the max (which was the original heuristic, but misreads
        # F-statistic decimal parts as eta² — see sensitivity_report.md
        # atlas-009 leverage flag).
        nums = [float(x) for x in re.findall(r"\b0?\.\d+\b", val)]
        if not nums:
            return None, None
        eta2 = nums[0]
        if eta2 >= 1.0 or eta2 <= 0:
            return None, None
        d = 2.0 * math.sqrt(eta2 / (1.0 - eta2))
        # Cohen's d SE approximation: sqrt(4/n + d²/(2n))
        se = math.sqrt(4.0 / n + (d * d) / (2.0 * n))
        return d, se

    # F-statistic — handle two metric-label conventions:
    #   "f-statistic..." with F(df1,df2)=val in value field, OR
    #   "f-N-M" where the df-within is encoded directly in the metric label
    f_metric_match = re.match(r"f-?(\d+)-?(\d+)", metric)
    if "f-statistic" in metric or f_metric_match:
        # Try to extract F value from the value field (with or without F() syntax)
        f_matches = re.findall(r"F\s*\([^)]*\)\s*=\s*([\d.]+)", val)
        if not f_matches:
            f_matches = re.findall(r"=\s*([\d.]+)", val)
        if not f_matches and v is not None:
            f = v
        elif f_matches:
            f = float(f_matches[0])
        else:
            return None, None
        # df_within: from the metric label if encoded ("f-1-235"), else
        # fall back to (n - groups). Default to df_within = max(n-2, 1).
        if f_metric_match:
            df_within = max(int(f_metric_match.group(2)), 1)
        else:
            df_within = max(n - 2, 1)
        eta2_p = f / (f + df_within)
        if eta2_p >= 1.0 or eta2_p <= 0:
            return None, None
        d = 2.0 * math.sqrt(eta2_p / (1.0 - eta2_p))
        # Cap implausibly large d at 5.0 — beyond that we're certainly seeing
        # reporting artifact, not a real effect size.
        if d > 5.0:
            return None, None
        se = math.sqrt(4.0 / n + (d * d) / (2.0 * n))
        return d, se

    if "t-statistic" in metric:
        # Two-sample t: convert via r = t / sqrt(t^2 + df), then d = 2r/sqrt(1-r²)
        if v is None:
            return None, None
        t = abs(v)
        df = max(n - 2, 1)
        r_val = t / math.sqrt(t * t + df)
        if abs(r_val) >= 1.0:
            return None, None
        d = 2.0 * r_val / math.sqrt(1.0 - r_val * r_val)
        if d > 5.0:
            return None, None
        se = math.sqrt(4.0 / n + (d * d) / (2.0 * n))
        return d, se

    if "cohens-d" in metric or "cohen-d" in metric or metric == "d":
        if v is None:
            return None, None
        d = v
        if abs(d) > 5.0:
            return None, None
        se = math.sqrt(4.0 / n + (d * d) / (2.0 * n))
        return d, se

    if "odds-ratio" in metric or "log-odds-ratio" in metric:
        # OR + 95% CI bounds → log-OR with SE from CI; then d ≈ log-OR × sqrt(3)/π
        if v is None or v <= 0:
            return None, None
        ci_lower_raw = (r.get("effect_size_ci_lower") or "").strip()
        ci_upper_raw = (r.get("effect_size_ci_upper") or "").strip()
        try:
            ci_lower = float(ci_lower_raw)
            ci_upper = float(ci_upper_raw)
        except ValueError:
            return None, None
        if ci_lower <= 0 or ci_upper <= 0:
            return None, None
        log_or = math.log(v)
        se_log_or = (math.log(ci_upper) - math.log(ci_lower)) / (2.0 * 1.96)
        # Cox-Hasselblad (1989) / Chinn (2000) conversion
        d = log_or * math.sqrt(3.0) / math.pi
        se = se_log_or * math.sqrt(3.0) / math.pi
        return d, se

    if "standardized-beta" in metric or "beta" in metric and "unstand" not in metric:
        # β as standardized regression coefficient; t-value reported may give r
        # Rough: treat β as approximation to r, then convert r → d
        r_val = v
        if r_val is None or abs(r_val) >= 1.0:
            return None, None
        d = 2 * r_val / math.sqrt(1 - r_val * r_val)
        se = math.sqrt(4.0 / n + (d * d) / (2.0 * n))
        return d, se

    if "mean-diff" in metric or "unstandardized-mean-diff" in metric:
        # Need pooled SD to standardize; not always available
        # If the value field includes SDs, try to parse
        sd_matches = re.findall(r"SD\s*=\s*([\d.]+)", val)
        m_matches = re.findall(r"M[_a-z]*\s*=\s*([\d.]+)", val)
        if len(sd_matches) >= 2 and len(m_matches) >= 2:
            m1, m2 = float(m_matches[0]), float(m_matches[1])
            sd1, sd2 = float(sd_matches[0]), float(sd_matches[1])
            sd_pooled = math.sqrt((sd1 * sd1 + sd2 * sd2) / 2.0)
            if sd_pooled == 0:
                return None, None
            d = (m1 - m2) / sd_pooled
            se = math.sqrt(4.0 / n + (d * d) / (2.0 * n))
            return d, se

    return None, None


# -----------------------------------------------------------------------------
# DerSimonian-Laird tau estimator (random-effects MoM)
# -----------------------------------------------------------------------------

def dersimonian_laird(yi: list[float], si: list[float]) -> tuple[float, float]:
    """Return (mu_hat_fixed, tau2_hat) using fixed-effect weighted mean +
    DerSimonian-Laird method-of-moments estimator for between-study variance.
    """
    wi = [1.0 / (s * s) for s in si]
    sum_w = sum(wi)
    mu_fixed = sum(w * y for w, y in zip(wi, yi)) / sum_w
    q = sum(w * (y - mu_fixed) ** 2 for w, y in zip(wi, yi))
    k = len(yi)
    if k <= 1:
        return mu_fixed, 0.0
    df = k - 1
    c = sum_w - sum(w * w for w in wi) / sum_w
    if c <= 0:
        return mu_fixed, 0.0
    tau2 = max(0.0, (q - df) / c)
    return mu_fixed, tau2


# -----------------------------------------------------------------------------
# Bayesian Monte Carlo with weakly-informative priors
# -----------------------------------------------------------------------------

def half_normal_sample(sd: float) -> float:
    return abs(random.gauss(0.0, sd))


def normal_sample(mean: float, sd: float) -> float:
    return random.gauss(mean, sd)


def bayesian_pool(yi: list[float], si: list[float],
                  prior_mu_sd: float = 0.5,
                  prior_tau_sd: float = 0.3,
                  n_draws: int = N_MONTE_CARLO) -> dict:
    """Approximate Bayesian random-effects meta-analysis via importance sampling.

    1. Sample tau from prior (Half-Normal(0, prior_tau_sd))
    2. Compute random-effects weights and mu posterior conditional on tau
    3. Importance-weight by data likelihood
    4. Resample mu draws
    """
    mu_fixed, tau2_dl = dersimonian_laird(yi, si)
    tau_dl = math.sqrt(tau2_dl)

    draws = []
    log_weights = []
    for _ in range(n_draws):
        # Sample tau from prior, with proposal centered near DL estimate
        tau = half_normal_sample(max(prior_tau_sd, tau_dl + 0.05))
        # Conditional posterior of mu given tau (weakly-informative Normal prior)
        wi = [1.0 / (s * s + tau * tau) for s in si]
        sum_w = sum(wi)
        # Posterior of mu | tau, y under Normal(0, prior_mu_sd) prior on mu:
        post_prec = 1.0 / (prior_mu_sd ** 2) + sum_w
        post_mean = (sum(w * y for w, y in zip(wi, yi))) / post_prec
        post_sd = math.sqrt(1.0 / post_prec)
        mu = normal_sample(post_mean, post_sd)
        # Marginal log-likelihood: sum_i Normal(yi | mu, sqrt(si^2 + tau^2))
        ll = sum(
            -0.5 * math.log(2 * math.pi * (s * s + tau * tau))
            - 0.5 * ((y - mu) ** 2) / (s * s + tau * tau)
            for y, s in zip(yi, si)
        )
        draws.append((mu, tau))
        log_weights.append(ll)

    # Normalize weights
    max_lw = max(log_weights)
    weights = [math.exp(lw - max_lw) for lw in log_weights]
    sum_w_norm = sum(weights)
    weights = [w / sum_w_norm for w in weights]

    # Resample
    cum = []
    s = 0.0
    for w in weights:
        s += w
        cum.append(s)
    resampled_mu = []
    resampled_tau = []
    for _ in range(n_draws):
        u = random.random()
        idx = 0
        while idx < len(cum) and cum[idx] < u:
            idx += 1
        idx = min(idx, len(cum) - 1)
        resampled_mu.append(draws[idx][0])
        resampled_tau.append(draws[idx][1])

    resampled_mu.sort()
    resampled_tau.sort()
    n = len(resampled_mu)
    return {
        "mu_median": resampled_mu[n // 2],
        "mu_ci_lower": resampled_mu[int(n * 0.025)],
        "mu_ci_upper": resampled_mu[int(n * 0.975)],
        "tau_median": resampled_tau[n // 2],
        "tau_ci_lower": resampled_tau[int(n * 0.025)],
        "tau_ci_upper": resampled_tau[int(n * 0.975)],
        "p_mu_gt_zero": sum(1 for m in resampled_mu if m > 0) / n,
        "p_mu_gt_practical": sum(1 for m in resampled_mu if m > 0.20) / n,
        "k_studies": len(yi),
        "method": "approximate-bayesian-importance-sampling",
        "n_draws": n_draws,
    }


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    if not PILOT_PATH.exists():
        print(f"ERROR: {PILOT_PATH} missing", file=sys.stderr)
        return 1

    rows = parse_pilot(PILOT_PATH)
    print(f"[pilot-meta] Parsed {len(rows)} approximate effect sizes")

    by_tech: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_tech[r["technique_taxonomy_id"]].append(r)

    results = []
    for tid, recs in sorted(by_tech.items()):
        if len(recs) < 2:
            print(f"  {tid}: k={len(recs)} — skip (need k≥2)")
            continue
        yi = [r["d_approx"] for r in recs]
        si = [r["se_approx"] for r in recs]
        post = bayesian_pool(yi, si)
        post["technique_taxonomy_id"] = tid
        post["study_ids"] = ";".join(r["study_id"] for r in recs)
        results.append(post)
        print(f"  {tid}: k={post['k_studies']}, "
              f"mu={post['mu_median']:.3f} [{post['mu_ci_lower']:.3f}, {post['mu_ci_upper']:.3f}], "
              f"tau={post['tau_median']:.3f}, "
              f"P(mu>0)={post['p_mu_gt_zero']:.3f}, "
              f"P(mu>0.2)={post['p_mu_gt_practical']:.3f}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if results:
        fields = list(results[0].keys())
        with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in results:
                w.writerow({k: r.get(k, "") for k in fields})
        print(f"\n[pilot-meta] Wrote {len(results)} per-technique posteriors to {OUTPUT_PATH}")

    print()
    print("Important caveats:")
    print("- This pilot uses pure-stdlib importance sampling, not Stan MCMC.")
    print("- Effect-size conversion is approximate (eta² → d, F → d, β → r → d).")
    print("- k=2-4 per technique → very wide posterior intervals expected.")
    print("- For preprint-quality inference, run analysis/02_primary_meta_analysis.R")
    print("  with R + brms + cmdstanr after Phase 2 scale-up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
