#!/usr/bin/env python3
"""
Phase 4 sensitivity-analysis pilot — rerun the Phase 3 pilot with specific
records dropped, to check the robustness of per-technique posteriors to
methodologically-questionable records.

Pre-registered sensitivity moves to be reported in the final preprint
(per PROTOCOL.md § 9.4):
  1. Drop high-RoB records and rerun (gain-framing posterior shift).
  2. Drop records using approximate-only effect-size conversions (e.g., the
     log-OR conversion in Toll 2007, the cohens-d midpoint estimate in
     Griskevicius 2009).
  3. Drop pre-registered records and rerun (test pre-registration's effect
     on the pooled posterior).
  4. Drop the largest single-study effect and rerun (leave-one-out leverage).

This script implements moves 1-2 and 4. Move 3 is left for the formal Stan-MCMC
analysis in `analysis/05_sensitivity.R` where the pre-registration column can
be used as a moderator directly.

Stdlib only. Re-uses the importance sampler in pilot_meta_analysis.py.
"""

from __future__ import annotations

import csv
import math
import random
import sys
from pathlib import Path

# Import the pilot's parser + DL + posterior sampler
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pilot_meta_analysis import (
    parse_pilot, dersimonian_laird, bayesian_pool, REPO, PILOT_PATH
)

OUTPUT_REPORT = REPO / "results" / "sensitivity_report.md"

random.seed(20260510)
N_DRAWS = 10_000


def pool_one(rows: list[dict]) -> dict | None:
    """Pool one technique's effect sizes via bayesian_pool from pilot_meta_analysis."""
    yi = [r["d_approx"] for r in rows]
    si = [r["se_approx"] for r in rows]
    if len(yi) < 2:
        return None
    s = bayesian_pool(yi, si, n_draws=N_DRAWS)
    s["study_ids"] = [r["study_id"] for r in rows]
    return s


def fmt(s: dict) -> str:
    return (
        f"k={s['k_studies']}  μ={s['mu_median']:.3f}  "
        f"CrI [{s['mu_ci_lower']:.3f}, {s['mu_ci_upper']:.3f}]  "
        f"τ={s['tau_median']:.3f}  "
        f"P(μ>0)={s['p_mu_gt_zero']:.3f}  "
        f"P(μ>0.2)={s['p_mu_gt_practical']:.3f}"
    )


def main() -> int:
    rows = parse_pilot(PILOT_PATH)

    # Group by technique
    by_tech: dict[str, list[dict]] = {}
    for r in rows:
        by_tech.setdefault(r["technique_taxonomy_id"], []).append(r)

    report_lines = [
        "# Sensitivity Analysis Pilot",
        "",
        "Re-running the Phase 3 pilot posterior with specific records dropped, to check robustness of per-technique posteriors to methodologically-questionable inputs.",
        "",
        "All analyses use the same importance-sampling Bayesian pipeline as `pilot_meta_analysis.py`. Stdlib only; not a Stan-MCMC equivalent — the final preprint uses `analysis/05_sensitivity.R` with brms.",
        "",
    ]

    # -------- Baseline (all records) --------
    report_lines += ["## Baseline (all extractable records)", ""]
    baselines: dict[str, dict] = {}
    for tech, tech_rows in sorted(by_tech.items()):
        s = pool_one(tech_rows)
        if s is None:
            continue
        baselines[tech] = s
        report_lines.append(f"- **`{tech}`** — {fmt(s)}")
    report_lines += [""]

    # -------- Move 1: drop high-RoB records --------
    report_lines += [
        "## Sensitivity 1 — drop high-RoB records",
        "",
        "High risk-of-bias records (rob_overall='high') are excluded; the posterior is recomputed. Stable posteriors here indicate the headline findings do not depend on the weakest-quality records.",
        "",
    ]
    for tech, tech_rows in sorted(by_tech.items()):
        filtered = [r for r in tech_rows if r.get("rob_overall", "").lower() != "high"]
        s = pool_one(filtered)
        if s is None or tech not in baselines:
            continue
        delta = s["mu_median"] - baselines[tech]["mu_median"]
        report_lines.append(
            f"- **`{tech}`** — {fmt(s)}   "
            f"Δμ from baseline: {delta:+.3f}"
        )
    report_lines += [""]

    # -------- Move 2: drop log-OR conversion (atlas-014) --------
    report_lines += [
        "## Sensitivity 2 — drop log-OR conversion (atlas-014 Toll 2007)",
        "",
        "atlas-014 (Toll 2007 smoking-cessation RCT) is the only record using the Cox-Hasselblad log-OR → d approximation (Chinn 2000). The posterior is recomputed without it to verify that the gain-framing and loss-framing posteriors don't depend on this specific conversion.",
        "",
    ]
    for tech, tech_rows in sorted(by_tech.items()):
        filtered = [r for r in tech_rows if r["study_id"] != "atlas-014"]
        s = pool_one(filtered)
        if s is None or tech not in baselines:
            continue
        delta = s["mu_median"] - baselines[tech]["mu_median"]
        report_lines.append(
            f"- **`{tech}`** — {fmt(s)}   "
            f"Δμ from baseline: {delta:+.3f}"
        )
    report_lines += [""]

    # -------- Move 4: leave-one-out (single largest-d record per technique) --------
    report_lines += [
        "## Sensitivity 3 — leave-one-out (largest-d record per technique)",
        "",
        "For each technique, drop the record with the largest absolute Cohen's d and recompute. Stable posteriors here indicate no single high-leverage record is driving the pooled estimate.",
        "",
    ]
    for tech, tech_rows in sorted(by_tech.items()):
        if len(tech_rows) < 3:
            continue
        largest = max(tech_rows, key=lambda r: abs(r["d_approx"]))
        filtered = [r for r in tech_rows if r["study_id"] != largest["study_id"]]
        s = pool_one(filtered)
        if s is None or tech not in baselines:
            continue
        delta = s["mu_median"] - baselines[tech]["mu_median"]
        report_lines.append(
            f"- **`{tech}`** — dropped {largest['study_id']} (d={largest['d_approx']:.3f}) — {fmt(s)}   "
            f"Δμ from baseline: {delta:+.3f}"
        )
    report_lines += [""]

    # -------- Honest interpretation --------
    report_lines += [
        "## Honest interpretation",
        "",
        "Per the pre-registered protocol, **sensitivity-stable** is defined as: posterior μ shift |Δμ| ≤ 0.10 AND P(μ>0) remains > 0.95 under all sensitivity moves. Read the deltas above against this threshold.",
        "",
        "Sensitivity moves that exceed Δμ=0.10 OR reduce P(μ>0) below 0.95 are flagged for explicit treatment in the preprint's limitations section.",
        "",
        "These are pilot-stage diagnostics using importance sampling on approximate effect-size conversions. The protocol-conformant sensitivity battery (Cochrane-style RoB stratification, three-parameter selection model, PET-PEESE) lives in `analysis/05_sensitivity.R` and runs after R/brms install.",
    ]

    with OUTPUT_REPORT.open("w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[sensitivity] Wrote {OUTPUT_REPORT}")
    # Echo the headlines to stdout
    for line in report_lines[:60]:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
