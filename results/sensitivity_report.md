# Sensitivity Analysis Pilot

Re-running the Phase 3 pilot posterior with specific records dropped, to check robustness of per-technique posteriors to methodologically-questionable inputs.

All analyses use the same importance-sampling Bayesian pipeline as `pilot_meta_analysis.py`. Stdlib only; not a Stan-MCMC equivalent — the final preprint uses `analysis/05_sensitivity.R` with brms.

## Baseline (all extractable records)

- **`commitment-consistency`** — k=2  μ=0.590  CrI [0.331, 0.782]  τ=0.089  P(μ>0)=0.999  P(μ>0.2)=0.993
- **`extreme-anchor`** — k=2  μ=0.435  CrI [0.043, 0.745]  τ=0.269  P(μ>0)=0.983  P(μ>0.2)=0.914
- **`gain-framing`** — k=9  μ=0.474  CrI [0.305, 0.642]  τ=0.301  P(μ>0)=1.000  P(μ>0.2)=0.997
- **`loss-framing`** — k=7  μ=0.327  CrI [0.249, 0.410]  τ=0.047  P(μ>0)=1.000  P(μ>0.2)=0.999
- **`regulatory-fit`** — k=3  μ=0.484  CrI [0.346, 0.632]  τ=0.068  P(μ>0)=1.000  P(μ>0.2)=0.997
- **`social-proof`** — k=2  μ=0.515  CrI [-0.494, 1.408]  τ=1.600  P(μ>0)=0.845  P(μ>0.2)=0.738

## Sensitivity 1 — drop high-RoB records

High risk-of-bias records (rob_overall='high') are excluded; the posterior is recomputed. Stable posteriors here indicate the headline findings do not depend on the weakest-quality records.

- **`extreme-anchor`** — k=2  μ=0.440  CrI [0.048, 0.724]  τ=0.272  P(μ>0)=0.983  P(μ>0.2)=0.917   Δμ from baseline: +0.005
- **`gain-framing`** — k=9  μ=0.472  CrI [0.306, 0.642]  τ=0.301  P(μ>0)=1.000  P(μ>0.2)=0.998   Δμ from baseline: -0.002
- **`loss-framing`** — k=7  μ=0.328  CrI [0.249, 0.409]  τ=0.045  P(μ>0)=1.000  P(μ>0.2)=0.998   Δμ from baseline: +0.001
- **`regulatory-fit`** — k=2  μ=0.448  CrI [0.218, 0.638]  τ=0.082  P(μ>0)=0.998  P(μ>0.2)=0.979   Δμ from baseline: -0.036
- **`social-proof`** — k=2  μ=0.511  CrI [-0.526, 1.389]  τ=1.605  P(μ>0)=0.841  P(μ>0.2)=0.729   Δμ from baseline: -0.005

## Sensitivity 2 — drop log-OR conversion (atlas-014 Toll 2007)

atlas-014 (Toll 2007 smoking-cessation RCT) is the only record using the Cox-Hasselblad log-OR → d approximation (Chinn 2000). The posterior is recomputed without it to verify that the gain-framing and loss-framing posteriors don't depend on this specific conversion.

- **`commitment-consistency`** — k=2  μ=0.588  CrI [0.338, 0.779]  τ=0.089  P(μ>0)=0.999  P(μ>0.2)=0.993   Δμ from baseline: -0.002
- **`extreme-anchor`** — k=2  μ=0.440  CrI [0.048, 0.719]  τ=0.269  P(μ>0)=0.981  P(μ>0.2)=0.913   Δμ from baseline: +0.005
- **`gain-framing`** — k=8  μ=0.481  CrI [0.294, 0.669]  τ=0.319  P(μ>0)=1.000  P(μ>0.2)=0.997   Δμ from baseline: +0.007
- **`loss-framing`** — k=6  μ=0.324  CrI [0.239, 0.410]  τ=0.049  P(μ>0)=1.000  P(μ>0.2)=0.996   Δμ from baseline: -0.003
- **`regulatory-fit`** — k=3  μ=0.485  CrI [0.347, 0.635]  τ=0.071  P(μ>0)=1.000  P(μ>0.2)=0.997   Δμ from baseline: +0.001
- **`social-proof`** — k=2  μ=0.516  CrI [-0.508, 1.379]  τ=1.590  P(μ>0)=0.834  P(μ>0.2)=0.727   Δμ from baseline: +0.000

## Sensitivity 3 — leave-one-out (largest-d record per technique)

For each technique, drop the record with the largest absolute Cohen's d and recompute. Stable posteriors here indicate no single high-leverage record is driving the pooled estimate.

- **`gain-framing`** — dropped atlas-009 (d=1.309) — k=8  μ=0.342  CrI [0.263, 0.424]  τ=0.048  P(μ>0)=1.000  P(μ>0.2)=0.999   Δμ from baseline: -0.132
- **`loss-framing`** — dropped atlas-015 (d=0.519) — k=6  μ=0.319  CrI [0.236, 0.401]  τ=0.047  P(μ>0)=1.000  P(μ>0.2)=0.994   Δμ from baseline: -0.008
- **`regulatory-fit`** — dropped atlas-049 (d=0.606) — k=2  μ=0.448  CrI [0.226, 0.626]  τ=0.077  P(μ>0)=0.998  P(μ>0.2)=0.981   Δμ from baseline: -0.036

## Honest interpretation

Per the pre-registered protocol, **sensitivity-stable** is defined as: posterior μ shift |Δμ| ≤ 0.10 AND P(μ>0) remains > 0.95 under all sensitivity moves. Read the deltas above against this threshold.

Sensitivity moves that exceed Δμ=0.10 OR reduce P(μ>0) below 0.95 are flagged for explicit treatment in the preprint's limitations section.

These are pilot-stage diagnostics using importance sampling on approximate effect-size conversions. The protocol-conformant sensitivity battery (Cochrane-style RoB stratification, three-parameter selection model, PET-PEESE) lives in `analysis/05_sensitivity.R` and runs after R/brms install.