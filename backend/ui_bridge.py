"""Bridge between the React dashboard and the Python workspace.

`build_state` produces the JSON the dashboard renders; `handle_event` applies one UI
action. Streamlit (custom component) and FastAPI (/api/v1/ui/*) both use these, so the
dashboard behaves the same in either host.
"""

from __future__ import annotations

import base64
import binascii
import logging
from datetime import datetime, timezone
from typing import Any

from . import charts
from .document_loader import DocumentLoadError
from .experiments import IncompatibleRuns
from .root_cause import LABELS
from .schemas import to_jsonable
from .service import NotFound, Workspace
from .text_utils import truncate

log = logging.getLogger(__name__)

EMBEDDING_CHOICES = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/multi-qa-MiniLM-L6-cos-v1",
]


def _mode_view(mode) -> dict[str, Any] | None:
    if mode is None:
        return None
    return {
        "passed": mode.passed,
        "metrics": mode.metrics,
        "answer": mode.answer,
        "contexts": [truncate(c, 700) for c in mode.contexts],
        "retrieved": [
            {"chunk_id": r.chunk_id, "rank": r.rank, "score": r.score, "text": truncate(r.text, 700),
             "supports": r.supports, "coverage": r.coverage, "page": r.page_number}
            for r in mode.retrieved
        ],
        "latency_ms": mode.latency_ms,
        "estimated_cost": mode.estimated_cost,
        "error": mode.error,
    }


def _run_view(run, filenames: dict[str, str]) -> dict[str, Any]:
    s = run.summary or {}
    return {
        "run_id": run.run_id, "label": run.label, "created_at": run.created_at, "status": run.status,
        "document_id": run.document_id, "filename": filenames.get(run.document_id, "deleted document"),
        "config": run.configuration.to_dict(), "config_short": run.configuration.short(),
        "duration_ms": run.duration_ms, "parent_run_id": run.parent_run_id, "error": run.error,
        "questions": s.get("questions"), "passed": s.get("passed"), "pass_rate": s.get("pass_rate"),
        "headline": s.get("headline", {}), "diagnoses": s.get("diagnoses", {}),
        "modes": {m: {"pass_rate": v.get("pass_rate"), "passed": v.get("passed"), "measured": v.get("measured"),
                      "latency_ms_avg": v.get("latency_ms_avg"), "errors": v.get("errors"), "metrics": v.get("metrics")}
                  for m, v in s.get("modes", {}).items()},
        "top_recommendation": s.get("top_recommendation"), "review": s.get("review"),
        "environment": s.get("environment"), "question_types": s.get("question_types", {}),
    }


def _funnel(results) -> list[dict[str, Any]]:
    """Nested stages: every stage is a subset of the one before it."""
