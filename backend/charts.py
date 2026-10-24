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


def _stamp(run: EvaluationRun) -> str:
    try:
        return datetime.fromisoformat(run.created_at).strftime("%b %d %H:%M")
    except ValueError:
        return run.created_at[:16]


def _run_label(run: EvaluationRun, index: int) -> str:
    return f"Run {index}"


def _category_axis(**extra: Any) -> dict[str, Any]:
    # Run labels must stay categorical (Plotly would otherwise coerce "Run 1"-like strings to numbers).
    return dict(type="category", showgrid=False, zeroline=False, linecolor=GRID, tickfont=dict(size=11),
                fixedrange=True, **extra)


def trend_figures(runs: list[EvaluationRun], target: float = 0.8) -> dict[str, dict[str, Any]]:
    """One single-series spline chart per headline metric (the dashboard toggles between them)."""
    chronological = list(reversed(runs))[-12:]
    labels = [_run_label(r, i + 1) for i, r in enumerate(chronological)]
    figures = {}
    for key, (title, getter) in TREND_METRICS.items():
        values = [getter(r) for r in chronological]
        hover = [
            f"<b>{title}: {v:.0%}</b><br>{r.label or r.configuration.short()}<br>{lab} · {_stamp(r)}" if v is not None
            else f"<b>{title}: not measured</b><br>{lab} · {_stamp(r)}"
            for v, r, lab in zip(values, chronological, labels)
        ]
        fig = go.Figure(go.Scatter(
            x=labels, y=values, mode="lines+markers", line=dict(color=SERIES[0], width=2, shape="spline", smoothing=0.8),
            marker=dict(size=8, color=SERIES[0], line=dict(color="#ffffff", width=2)),
            fill="tozeroy", fillcolor="rgba(42,120,214,0.10)", hovertext=hover, hoverinfo="text",
            connectgaps=False, name=title,
        ))
        fig.add_hline(y=target, line=dict(color=INK_MUTED, width=1), opacity=0.6,
                      annotation_text=f"Target {target:.0%}", annotation_position="top left",
                      annotation_font=dict(size=10, color=INK_MUTED))
        fig.update_layout(**_base_layout(
            xaxis=_category_axis(),
            yaxis=dict(gridcolor=GRID, zeroline=False, range=[0, 1.05], tickformat=".0%", fixedrange=True,
                       tickfont=dict(size=11)),
            hovermode="x unified" if len(labels) > 1 else "closest",
        ))
        figures[key] = _to_json(fig)
    return figures


def mode_trend_figure(runs: list[EvaluationRun]) -> dict[str, Any]:
    """Pass rate of each test mode across runs (three series, legend + endpoint labels)."""
    chronological = list(reversed(runs))[-12:]
    labels = [_run_label(r, i + 1) for i, r in enumerate(chronological)]
    fig = go.Figure()
    names = {"retriever": "Retriever-only", "generator": "Generator-only", "end_to_end": "End-to-end"}
    for color, (mode, name) in zip(SERIES, names.items()):
        values = [r.summary.get("modes", {}).get(mode, {}).get("pass_rate") for r in chronological]
        fig.add_trace(go.Scatter(
            x=labels, y=values, name=name, mode="lines+markers",
            line=dict(color=color, width=2, shape="spline", smoothing=0.6),
            marker=dict(size=8, color=color, line=dict(color="#ffffff", width=2)),
            hovertemplate=f"{name}: %{{y:.0%}}<extra></extra>",
        ))
    fig.update_layout(**_base_layout(
        showlegend=True, legend=dict(orientation="h", y=1.12, x=0, font=dict(size=11)),
        margin=dict(l=44, r=16, t=32, b=36), hovermode="x unified", xaxis=_category_axis(),
        yaxis=dict(gridcolor=GRID, zeroline=False, range=[0, 1.05], tickformat=".0%", fixedrange=True,
                   tickfont=dict(size=11)),
    ))
    return _to_json(fig)


def runs_bar_figure(runs: list[EvaluationRun], highlight_run_id: str | None) -> dict[str, Any]:
    """Pass rate per run; the selected run is emphasised, the rest are muted."""
    chronological = list(reversed(runs))[-8:]
    labels = [_run_label(r, i + 1) for i, r in enumerate(chronological)]
    values = [r.summary.get("pass_rate") or 0 for r in chronological]
    colors = [SERIES[0] if r.run_id == highlight_run_id else MUTED_BAR for r in chronological]
    fig = go.Figure(go.Bar(
        x=labels, y=values, marker=dict(color=colors, cornerradius=4), width=0.62,
        hovertext=[f"<b>{v:.0%} pass</b><br>{r.label or r.configuration.short()}" for v, r in zip(values, chronological)],
        hoverinfo="text",
    ))
    fig.update_layout(**_base_layout(
        margin=dict(l=36, r=8, t=8, b=28), bargap=0.3, xaxis=_category_axis(),
        yaxis=dict(gridcolor=GRID, zeroline=False, range=[0, 1], tickformat=".0%", fixedrange=True, nticks=4,
                   tickfont=dict(size=10)),
    ))
    return _to_json(fig)


def failure_donut(summary: dict[str, Any], labels: dict[str, str]) -> dict[str, Any] | None:
    diagnoses = {k: v for k, v in summary.get("diagnoses", {}).items() if k != "PASS" and v}
    if not diagnoses:
        return None
    order = [k for k in DIAGNOSIS_COLORS if k in diagnoses]
    total = sum(diagnoses.values())
    fig = go.Figure(go.Pie(
        labels=[labels.get(k, k) for k in order], values=[diagnoses[k] for k in order],
        marker=dict(colors=[DIAGNOSIS_COLORS[k] for k in order], line=dict(color="#ffffff", width=2)),
        hole=0.72, sort=False, direction="clockwise", textinfo="none",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig.update_layout(**_base_layout(
        margin=dict(l=4, r=4, t=4, b=4),
        annotations=[dict(text=f"<b style='font-size:22px'>{total}</b><br>failing", showarrow=False,
                          font=dict(size=11, color=INK_MUTED), x=0.5, y=0.5)],
    ))
    return _to_json(fig)


def comparison_figure(comparison: dict[str, Any]) -> dict[str, Any]:
    rows = [r for r in comparison["metrics"] if r["mode"] in ("overall", "retriever", "generator", "end_to_end")
            and r["key"] not in ("latency_ms_avg", "cost_total") and (r["baseline"] is not None or r["candidate"] is not None)]
    rows = list(reversed(rows))
    names = [r["metric"] for r in rows]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=names, x=[r["baseline"] for r in rows], name="Baseline", orientation="h",
        marker=dict(color=BASELINE, cornerradius=4), hovertemplate="Baseline: %{x:.2f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=names, x=[r["candidate"] for r in rows], name="Candidate", orientation="h",
        marker=dict(color=SERIES[0], cornerradius=4), hovertemplate="Candidate: %{x:.2f}<extra></extra>",
    ))
    fig.update_layout(**_base_layout(
        barmode="group", bargap=0.35, bargroupgap=0.12, showlegend=True,
        legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11), traceorder="reversed"),
        margin=dict(l=210, r=16, t=30, b=30),
        xaxis=dict(gridcolor=GRID, showgrid=True, zeroline=False, range=[0, 1.05], fixedrange=True,
                   tickfont=dict(size=11)),
        yaxis=dict(showgrid=False, zeroline=False, fixedrange=True, tickfont=dict(size=11)),
        height=max(260, 46 * len(rows) + 60),
    ))
    return _to_json(fig)
