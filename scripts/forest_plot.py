#!/usr/bin/env python3
"""
Pure-stdlib SVG forest-plot generator for the Atlas's per-technique
posterior estimates.

Reads results/pilot_posterior_summaries.csv and outputs figures/forest_pilot.svg.

For real-data forest plots after Phase 3 R/brms runs, the same generator
reads results/posterior_summaries.csv and outputs figures/forest_main.svg.

No matplotlib / numpy / scipy dependency — emits valid SVG by string template.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO / "results" / "pilot_posterior_summaries.csv"
DEFAULT_OUTPUT = REPO / "figures" / "forest_pilot.svg"


def parse_posteriors(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                rows.append({
                    "technique": r["technique_taxonomy_id"],
                    "k": int(r.get("k_studies") or r.get("n_studies") or 0),
                    "mu_median": float(r["mu_median"]),
                    "mu_lo": float(r.get("mu_ci_lower") or r["mu_ci95_lower"]),
                    "mu_hi": float(r.get("mu_ci_upper") or r["mu_ci95_upper"]),
                    "p_mu_gt_zero": float(r.get("p_mu_gt_zero", "0.5") or 0.5),
                    "p_mu_gt_practical": float(r.get("p_mu_gt_practical", "0.0") or 0.0),
                })
            except (KeyError, ValueError) as e:
                print(f"  skipping row {r}: {e}", file=sys.stderr)
    return rows


def scale_x(value: float, x_min: float, x_max: float, plot_x: float, plot_w: float) -> float:
    """Linear scale from data-coordinates to SVG pixel-coordinates."""
    if x_max == x_min:
        return plot_x + plot_w / 2
    return plot_x + plot_w * (value - x_min) / (x_max - x_min)


def render_forest(rows: list[dict], output_path: Path, title: str = "") -> None:
    if not rows:
        print("No rows to plot", file=sys.stderr)
        return

    # Plot dimensions
    width = 880
    row_h = 56
    margin_top = 90 if title else 60
    margin_bottom = 90
    plot_x_label = 280
    plot_x_data = 320
    plot_w = 360
    plot_x_stats = plot_x_data + plot_w + 40
    height = margin_top + row_h * len(rows) + margin_bottom

    # Determine x-axis range (with padding)
    all_los = [r["mu_lo"] for r in rows]
    all_his = [r["mu_hi"] for r in rows]
    x_min = min(all_los + [0]) - 0.05
    x_max = max(all_his + [0]) + 0.05

    # Build SVG
    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Inter, -apple-system, sans-serif" font-size="13">'
    )
    parts.append('<style>'
                 '.title{font-size:18px;font-weight:600;fill:#1a1a1a}'
                 '.header{font-size:11px;font-weight:600;fill:#666;text-transform:uppercase;letter-spacing:.05em}'
                 '.tech{font-size:14px;font-weight:500;fill:#1a1a1a}'
                 '.k{font-size:11px;fill:#888}'
                 '.stat{font-size:12px;fill:#444;font-variant-numeric:tabular-nums}'
                 '.axis{stroke:#bbb;stroke-width:1}'
                 '.ref{stroke:#d0d0d0;stroke-width:1;stroke-dasharray:3 3}'
                 '.ci{stroke:#2c5282;stroke-width:2}'
                 '.point{fill:#2c5282;stroke:#fff;stroke-width:1.5}'
                 '.caption{font-size:11px;fill:#666}'
                 '</style>')

    if title:
        parts.append(f'<text x="40" y="34" class="title">{title}</text>')

    # Column headers
    header_y = margin_top - 20
    parts.append(f'<text x="40" y="{header_y}" class="header">Technique</text>')
    parts.append(f'<text x="{plot_x_data + plot_w / 2}" y="{header_y}" class="header" text-anchor="middle">Posterior μ (Cohen\'s d scale)</text>')
    parts.append(f'<text x="{plot_x_stats}" y="{header_y}" class="header">Estimate [95% CrI]</text>')

    # Y-position for each row
    for i, row in enumerate(rows):
        y = margin_top + row_h * i + row_h / 2

        # Technique label
        parts.append(
            f'<text x="40" y="{y + 4}" class="tech">{row["technique"]}</text>'
        )
        parts.append(
            f'<text x="40" y="{y + 22}" class="k">k = {row["k"]} studies</text>'
        )

        # Reference line at zero (if within range)
        zero_x = scale_x(0, x_min, x_max, plot_x_data, plot_w)
        # CI bar
        ci_lo_x = scale_x(row["mu_lo"], x_min, x_max, plot_x_data, plot_w)
        ci_hi_x = scale_x(row["mu_hi"], x_min, x_max, plot_x_data, plot_w)
        median_x = scale_x(row["mu_median"], x_min, x_max, plot_x_data, plot_w)

        parts.append(
            f'<line x1="{ci_lo_x}" y1="{y}" x2="{ci_hi_x}" y2="{y}" class="ci"/>'
        )
        parts.append(
            f'<line x1="{ci_lo_x}" y1="{y-6}" x2="{ci_lo_x}" y2="{y+6}" class="ci"/>'
        )
        parts.append(
            f'<line x1="{ci_hi_x}" y1="{y-6}" x2="{ci_hi_x}" y2="{y+6}" class="ci"/>'
        )
        parts.append(
            f'<circle cx="{median_x}" cy="{y}" r="6" class="point"/>'
        )

        # Stats column
        stat_str = f'{row["mu_median"]:+.3f} [{row["mu_lo"]:+.3f}, {row["mu_hi"]:+.3f}]'
        prob_str = f'P(μ>0) = {row["p_mu_gt_zero"]:.2f}'
        parts.append(
            f'<text x="{plot_x_stats}" y="{y + 4}" class="stat">{stat_str}</text>'
        )
        parts.append(
            f'<text x="{plot_x_stats}" y="{y + 22}" class="stat" fill="#888">{prob_str}</text>'
        )

    # X-axis at bottom
    axis_y = margin_top + row_h * len(rows) + 15
    parts.append(
        f'<line x1="{plot_x_data}" y1="{axis_y}" x2="{plot_x_data + plot_w}" y2="{axis_y}" class="axis"/>'
    )

    # X-axis ticks at sensible intervals
    tick_values = []
    step = 0.5 if (x_max - x_min) > 1.0 else 0.25
    v = x_min
    while v <= x_max + 1e-9:
        tick_values.append(round(v, 2))
        v += step
    for tv in tick_values:
        tx = scale_x(tv, x_min, x_max, plot_x_data, plot_w)
        parts.append(f'<line x1="{tx}" y1="{axis_y}" x2="{tx}" y2="{axis_y + 5}" class="axis"/>')
        parts.append(f'<text x="{tx}" y="{axis_y + 20}" class="stat" text-anchor="middle">{tv:+.2f}</text>')

    # Reference line at zero across all rows
    zero_x = scale_x(0, x_min, x_max, plot_x_data, plot_w)
    parts.append(
        f'<line x1="{zero_x}" y1="{margin_top - 5}" x2="{zero_x}" y2="{axis_y}" class="ref"/>'
    )

    # Caption
    cap_y = axis_y + 50
    parts.append(
        f'<text x="40" y="{cap_y}" class="caption">'
        f'Posterior median + 95% credible interval per pre-registered Bayesian random-effects model. '
        f'CrI from importance-sampled posterior; pilot k = 2 per technique → wide intervals expected.'
        f'</text>'
    )
    parts.append(
        f'<text x="40" y="{cap_y + 16}" class="caption">'
        f'Final Phase-3 forest plot will use brms-Stan inference with k = 20-100 per technique. '
        f'Reference line at μ = 0 (no effect).'
        f'</text>'
    )

    parts.append('</svg>')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(parts), encoding="utf-8")
    print(f"Forest plot written to {output_path}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(DEFAULT_INPUT))
    p.add_argument("--output", default=str(DEFAULT_OUTPUT))
    p.add_argument("--title", default="closing-evidence-atlas — Phase 3 pilot posteriors")
    args = p.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: {input_path} missing", file=sys.stderr)
        return 1

    rows = parse_posteriors(input_path)
    if not rows:
        print("No posterior rows to plot", file=sys.stderr)
        return 1

    render_forest(rows, Path(args.output), title=args.title)
    return 0


if __name__ == "__main__":
    sys.exit(main())
