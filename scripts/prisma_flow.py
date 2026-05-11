#!/usr/bin/env python3
"""
PRISMA 2020 flow-diagram generator for the Closing Evidence Atlas.

Emits a self-contained SVG (no D3, no matplotlib) showing the pipeline from
12,416 raw search records through deduplication, Stage-1 screening, Phase 1.5
OA classification, Phase 2 extraction, and Phase 3 meta-analysis eligibility.

Numbers are hard-coded against the current Atlas state (post-commit 5b48d60).
Regenerate after each Phase 2 expansion that materially shifts the funnel.

Stdlib only.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUTPUT = REPO / "figures" / "prisma_flow.svg"


# --- Box specification (top-down) --------------------------------------------
# Each box: (label-lines, y-position, width, side-note-or-None)
# Side notes (excluded counts) sit to the right of the main flow.
MAIN_BOXES = [
    {
        "lines": [
            "Records identified via",
            "database searches",
            "n = 12,416",
        ],
        "y": 30,
    },
    {
        "lines": [
            "Records after duplicate removal",
            "n = 11,785",
        ],
        "y": 130,
        "side_note": [
            "Duplicates removed",
            "n = 631",
        ],
    },
    {
        "lines": [
            "Records screened (Stage-1)",
            "title + abstract",
            "n = 8,839 explicitly classified",
        ],
        "y": 230,
        "side_note": [
            "Low-priority deferred",
            "(score < 0.10, Dev. 005)",
            "n = 6,710",
        ],
    },
    {
        "lines": [
            "Records included for Stage-2",
            "n = 572",
        ],
        "y": 360,
        "side_note": [
            "Stage-1 excluded",
            "n = 8,123",
            "(heuristic + LLM screen)",
        ],
    },
    {
        "lines": [
            "Phase 1.5 OA accessibility check",
            "n = 141 OA with retrievable PDF",
            "(25% of Stage-1 includes)",
        ],
        "y": 480,
        "side_note": [
            "Closed-access deferred",
            "n = 431",
            "(pending institutional access)",
        ],
    },
    {
        "lines": [
            "Phase 2 records extracted",
            "n = 44",
        ],
        "y": 600,
        "side_note": [
            "OA records pending extraction",
            "n = 97 (LOW + UNKNOWN tier)",
            "8 HIGH-tier remaining",
        ],
    },
    {
        "lines": [
            "Phase 3 meta-analysis eligible",
            "n = 20 records, 6 techniques",
            "gain-framing k=9, loss-framing k=7,",
            "regulatory-fit k=3, three at k=2",
        ],
        "y": 720,
        "side_note": [
            "Extracted but not pooled",
            "n = 24",
            "(systematic reviews, unable-to-access,",
            "non-convertible effect-size metrics)",
        ],
    },
]


def render_box(label_lines: list[str], x: float, y: float, w: float, h: float, fill: str = "#fafafa") -> str:
    """Render a rectangular box with multi-line label centered inside."""
    text_x = x + w / 2
    n_lines = len(label_lines)
    line_h = 18
    block_h = n_lines * line_h
    first_baseline = y + (h - block_h) / 2 + 14
    out = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="6" ry="6" fill="{fill}" stroke="#333" stroke-width="1.5"/>',
    ]
    for i, line in enumerate(label_lines):
        ty = first_baseline + i * line_h
        weight = "600" if i == 0 else "400"
        out.append(
            f'<text x="{text_x:.1f}" y="{ty:.1f}" '
            f'text-anchor="middle" font-family="-apple-system, system-ui, sans-serif" '
            f'font-size="13" font-weight="{weight}" fill="#1a1a1a">{escape_xml(line)}</text>'
        )
    return "\n  ".join(out)


def render_side_note(lines: list[str], x: float, y: float, w: float, h: float) -> str:
    """Side-note dashed box for excluded-counts."""
    text_x = x + 12
    line_h = 16
    block_h = len(lines) * line_h
    first_baseline = y + (h - block_h) / 2 + 12
    out = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="4" ry="4" fill="#fefcf5" stroke="#999" stroke-width="1" stroke-dasharray="4 3"/>',
    ]
    for i, line in enumerate(lines):
        ty = first_baseline + i * line_h
        weight = "600" if i == 0 else "400"
        out.append(
            f'<text x="{text_x:.1f}" y="{ty:.1f}" '
            f'font-family="-apple-system, system-ui, sans-serif" '
            f'font-size="11" font-weight="{weight}" fill="#555">{escape_xml(line)}</text>'
        )
    return "\n  ".join(out)


def render_arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="#333" stroke-width="1.5" marker-end="url(#arrowhead)"/>'
    )


def escape_xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> int:
    width = 820
    height = 880
    main_x = 60
    main_w = 360
    side_x = 480
    side_w = 280

    # Compute box heights from line counts
    for box in MAIN_BOXES:
        box["h"] = max(60, 24 + len(box["lines"]) * 18)
        if box.get("side_note"):
            box["side_h"] = max(50, 16 + len(box["side_note"]) * 16)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" fill="white">',
        '<defs>',
        '  <marker id="arrowhead" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="8" markerHeight="8" orient="auto">',
        '    <path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/>',
        '  </marker>',
        '</defs>',
        # Title
        '<text x="410" y="20" text-anchor="middle" '
        'font-family="-apple-system, system-ui, sans-serif" '
        'font-size="14" font-weight="700" fill="#1a1a1a">'
        'PRISMA 2020 Flow — Closing Evidence Atlas (post 5b48d60)</text>',
    ]

    # Draw main flow boxes + arrows + side notes
    prev_box_y2 = None
    for box in MAIN_BOXES:
        y = box["y"]
        h = box["h"]
        svg_parts.append(render_box(box["lines"], main_x, y, main_w, h))
        if prev_box_y2 is not None:
            svg_parts.append(render_arrow(
                main_x + main_w / 2, prev_box_y2,
                main_x + main_w / 2, y - 2,
            ))
        if box.get("side_note"):
            side_y = y + (h - box["side_h"]) / 2
            svg_parts.append(render_side_note(
                box["side_note"], side_x, side_y, side_w, box["side_h"],
            ))
            # Arrow from main flow to side note
            svg_parts.append(render_arrow(
                main_x + main_w, y + h / 2,
                side_x - 2, side_y + box["side_h"] / 2,
            ))
        prev_box_y2 = y + h

    # Footer caption
    svg_parts.append(
        '<text x="410" y="860" text-anchor="middle" '
        'font-family="-apple-system, system-ui, sans-serif" '
        'font-size="10" fill="#666">'
        'Pre-registered systematic review. PROTOCOL.md committed before data inspection. '
        'See PROTOCOL_DEVIATIONS.md for transparent deviation log.</text>'
    )

    svg_parts.append('</svg>')

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"[prisma] Wrote {OUTPUT} ({sum(len(p) for p in svg_parts)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
