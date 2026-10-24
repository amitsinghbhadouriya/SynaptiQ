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

    def retrieval_ok(r) -> bool:
        mode = r.modes.get("retriever")
        if mode is None or mode.metrics.get("hit_at_k") is None:
            return True  # unanswerable: there is no evidence to retrieve
        return bool(mode.passed)

    stage_retrieval = [r for r in results if retrieval_ok(r)]
    stage_correct = [r for r in stage_retrieval if r.modes.get("end_to_end") and r.modes["end_to_end"].passed]
    stage_passed = [r for r in stage_correct if r.diagnosis == "PASS"]
    return [
        {"label": "Questions", "value": len(results)},
        {"label": "Retrieval OK", "value": len(stage_retrieval)},
        {"label": "End-to-end correct", "value": len(stage_correct)},
        {"label": "Passed all checks", "value": len(stage_passed)},
    ]


def build_state(ws: Workspace, selected_run_id: str | None = None) -> dict[str, Any]:
    documents = ws.storage.list_documents()
    filenames = {d.document_id: d.filename for d in documents}
    runs = ws.storage.list_runs()
    completed = [r for r in runs if r.status == "completed"]
    selected = next((r for r in runs if r.run_id == selected_run_id), None) or (completed[0] if completed else None)

    chunk_counts = ws.storage.chunk_counts()
    all_questions = ws.storage.list_questions()
    doc_views = []
    for d in documents:
        qs = [q for q in all_questions if q.document_id == d.document_id]
        doc_runs = [r for r in completed if r.document_id == d.document_id]
        doc_views.append({
            "document_id": d.document_id, "filename": d.filename, "file_type": d.file_type, "status": d.status,
            "created_at": d.created_at, "chars": len(d.text), "pages": d.metadata.get("pages"),
            "sections": d.metadata.get("section_count"), "chunks": d.metadata.get("chunk_count") or chunk_counts.get(d.document_id, 0),
            "questions": len([q for q in qs if q.review_status != "rejected"]),
            "approved": len([q for q in qs if q.review_status == "approved"]),
            "pending": len([q for q in qs if q.review_status == "pending"]),
            "runs": len(doc_runs), "last_pass_rate": doc_runs[0].summary.get("pass_rate") if doc_runs else None,
            "hash": d.content_hash[:10],
        })

    focus_doc = selected.document_id if selected else (documents[0].document_id if documents else None)
    questions = [q for q in all_questions if q.document_id == focus_doc]
    question_views = [{
        "question_id": q.question_id, "question": q.question, "reference_answer": q.reference_answer,
        "type": q.question_type, "review_status": q.review_status, "source": q.source,
        "evidence": [truncate(e.text, 400) for e in q.evidence], "supporting_chunk_ids": q.supporting_chunk_ids,
    } for q in questions]

    results_view, funnel, comparison, comparison_chart, donut = [], [], None, None, None
    if selected and selected.status == "completed":
        results = ws.storage.get_results(selected.run_id)
        q_by_id = {q.question_id: q for q in questions}
        for r in results:
            q = q_by_id.get(r.question_id)
            results_view.append({
                "question_id": r.question_id, "question": q.question if q else "(question removed)",
                "type": q.question_type if q else "", "reference_answer": q.reference_answer if q else "",
                "evidence": [truncate(e.text, 400) for e in q.evidence] if q else [],
                "diagnosis": r.diagnosis, "diagnosis_label": r.diagnosis_label, "diagnosis_reason": r.diagnosis_reason,
                "notes": r.evidence_notes, "recommendation": r.recommendation,
                "modes": {m: _mode_view(r.modes.get(m)) for m in ("retriever", "generator", "end_to_end")},
            })
        funnel = _funnel(results)
        donut = charts.failure_donut(selected.summary, LABELS)
        partner = next((r for r in runs if r.run_id == selected.parent_run_id and r.status == "completed"), None)
        if partner is None:
            partner = next((r for r in completed if r.document_id == selected.document_id
                            and r.created_at < selected.created_at), None)
