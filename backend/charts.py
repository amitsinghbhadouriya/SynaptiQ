"""Plotly figures for the dashboard, serialized to plain JSON for plotly.js.

Figures are built with the light-mode palette; the dashboard swaps each light hex for
its validated dark-mode step when the viewer switches theme (see PALETTE_DARK).
Palette: validated categorical order (blue, orange, aqua, yellow, magenta), one-hue
emphasis for single-series charts, neutral gray for baselines.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import plotly.graph_objects as go

from .schemas import EvaluationRun

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
PALETTE_DARK = {
    "#2a78d6": "#3987e5", "#eb6834": "#d95926", "#1baf7a": "#199e70", "#eda100": "#c98500",
    "#e87ba4": "#d55181", "#b8bcc6": "#4a4d57", "#9a9ca5": "#6e717b", "#d7e4f6": "#26364f",
}
MUTED_BAR = "#d7e4f6"   # de-emphasised bars (light blue-gray)
BASELINE = "#b8bcc6"    # baseline run in comparisons
NEUTRAL = "#9a9ca5"
INK_MUTED = "#898781"
GRID = "#ececf0"

DIAGNOSIS_COLORS = {  # colour follows the entity, never its rank
    "LIKELY_RETRIEVAL_FAILURE": SERIES[0],
    "LIKELY_GENERATION_FAILURE": SERIES[1],
    "LIKELY_COMBINED_FAILURE": SERIES[2],
    "PIPELINE_INTERACTION_FAILURE": SERIES[3],
    "CORRECT_BUT_UNGROUNDED": SERIES[4],
    "UNCERTAIN_REQUIRES_REVIEW": NEUTRAL,
}

TREND_METRICS = {
    "pass_rate": ("Pass rate", lambda r: r.summary.get("pass_rate")),
    "hit_at_k": ("Hit@k", lambda r: r.summary.get("headline", {}).get("hit_at_k")),
    "faithfulness": ("Faithfulness", lambda r: r.summary.get("headline", {}).get("faithfulness")),
    "answer_correctness": ("Answer correctness", lambda r: r.summary.get("headline", {}).get("answer_correctness")),
}


def _base_layout(**overrides: Any) -> dict[str, Any]:
    layout: dict[str, Any] = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter Variable, Inter, system-ui, sans-serif", size=12, color=INK_MUTED),
        margin=dict(l=44, r=16, t=12, b=36),
        hovermode="closest",
        hoverlabel=dict(bgcolor="#111318", bordercolor="#111318", font=dict(color="#f4f5f8", size=12)),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, linecolor=GRID, tickfont=dict(size=11), fixedrange=True),
        yaxis=dict(gridcolor=GRID, zeroline=False, tickfont=dict(size=11), fixedrange=True),
    )
    layout.update(overrides)
    return layout


def _to_json(fig: go.Figure) -> dict[str, Any]:
    return json.loads(fig.to_json())


