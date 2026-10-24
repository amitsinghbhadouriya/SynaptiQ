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
        if partner is not None:
            try:
                comparison = ws.compare(partner.run_id, selected.run_id, strict=False)
                comparison_chart = charts.comparison_figure(comparison)
            except (IncompatibleRuns, NotFound) as exc:
                comparison = {"error": str(exc)}

    doc_runs = [r for r in completed if not selected or r.document_id == selected.document_id]
    today = datetime.now(timezone.utc).date().isoformat()
    evaluated_today = sum(r.summary.get("questions", 0) for r in completed if r.created_at[:10] == today)

    return to_jsonable({
        "status": ws.status(),
        "documents": doc_views,
        "focus_document_id": focus_doc,
        "questions": question_views,
        "runs": [_run_view(r, filenames) for r in runs[:60]],
        "selected_run_id": selected.run_id if selected else None,
        "results": results_view,
        "funnel": funnel,
        "comparison": comparison,
        "evaluated_today": evaluated_today,
        "charts": {
            "trend": charts.trend_figures(doc_runs) if doc_runs else None,
            "modes": charts.mode_trend_figure(doc_runs) if doc_runs else None,
            "runs_bar": charts.runs_bar_figure(doc_runs, selected.run_id if selected else None) if doc_runs else None,
            "donut": donut,
            "comparison": comparison_chart,
        },
        "defaults": {"config": ws.default_config().to_dict(), "embedding_models": EMBEDDING_CHOICES,
                     "max_questions": ws.settings.max_questions},
        "labels": LABELS,
        "progress": ws.progress,
    })


def _decode_file(item: dict[str, Any]) -> tuple[str, bytes]:
    data = item.get("data") or ""
    if "," in data and data.startswith("data:"):
        data = data.split(",", 1)[1]
    try:
        return str(item.get("name") or "upload"), base64.b64decode(data, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("The uploaded file could not be decoded.") from exc


def handle_event(ws: Workspace, event: dict[str, Any]) -> dict[str, Any]:
    """Apply one dashboard action. Returns {"notice", "selected_run_id"?, "download"?, "navigate"?}."""
    kind = event.get("type")
    nonce = event.get("nonce")
    out: dict[str, Any] = {"nonce": nonce}

    def notice(level: str, message: str) -> dict[str, Any]:
        out["notice"] = {"level": level, "message": message, "nonce": nonce}
        return out

    try:
        if kind == "upload":
            created, reused, errors = [], [], []
            for item in event.get("files", []):
                try:
                    name, data = _decode_file(item)
                    document, is_new = ws.ingest(name, data)
                    (created if is_new else reused).append(document.filename)
                except DocumentLoadError as exc:
                    errors.append(f"{item.get('name')}: {exc.message}")
            if errors and not created and not reused:
                return notice("error", " ".join(errors))
            parts = []
            if created:
                parts.append(f"Indexed {', '.join(created)}.")
            if reused:
                parts.append(f"Already indexed: {', '.join(reused)}.")
            if errors:
                parts.append("Failed: " + " ".join(errors))
            return notice("warning" if errors else "success", " ".join(parts))

        if kind == "delete_document":
            ws.delete_document(event["document_id"])
            return notice("success", "Document, chunks, test questions and runs deleted.")

        if kind == "generate_tests":
            questions = ws.generate_test_set(event["document_id"], int(event.get("count", 10)), event.get("types"))
            return notice("success", f"Generated {len(questions)} candidate questions — review them before trusting scores.")

        if kind == "review":
            ws.review_question(event["question_id"], event.get("status"),
                               question=event.get("question"), reference_answer=event.get("reference_answer"))
            return notice("success", "Question updated.")

        if kind == "run_eval":
            config = ws.default_config(**(event.get("config") or {}))
            run = ws.run_evaluation(event["document_id"], config, event.get("modes"), label=event.get("label", ""))
            out["selected_run_id"] = run.run_id
            if run.status != "completed":
                return notice("error", f"Run failed: {run.error}")
            s = run.summary
            return notice("success", f"Run finished: {s['passed']}/{s['questions']} questions passed "
                                     f"({s['pass_rate']:.0%}) in {run.duration_ms / 1000:.1f}s.")

        if kind == "run_candidate":
            run = ws.run_recommendation(event["run_id"])
            out["selected_run_id"] = run.run_id
            if run.status != "completed":
                return notice("error", f"Candidate run failed: {run.error}")
            return notice("success", f"Candidate run finished: {run.summary['pass_rate']:.0%} pass rate. "
                                     "Compare it with the baseline under Reports.")

        if kind == "select_run":
            out["selected_run_id"] = event.get("run_id")
            return out

        if kind == "compare":
            comparison = ws.compare(event["baseline_run_id"], event["candidate_run_id"], strict=False)
            out["comparison"] = comparison
            out["comparison_chart"] = charts.comparison_figure(comparison)
            return notice("info", "Comparison ready." + (" " + comparison["warnings"][0] if comparison["warnings"] else ""))

        if kind == "export":
            filename, mime, content = ws.export(event["run_id"], event.get("format", "csv"))
            out["download"] = {"filename": filename, "mime": mime, "content": content, "nonce": nonce}
            return notice("success", f"Exported {filename} (also saved under reports/).")

        if kind == "load_demo":
            info = ws.load_demo()
            out["selected_run_id"] = info["candidate_run_id"] or info["baseline_run_id"]
            return notice("success", "Demo workspace ready: a baseline run and the recommended candidate were "
                                     "evaluated on the sample handbook.")

        if kind == "navigate":
            out["navigate"] = event.get("page")
            return out

        return notice("error", f"Unknown action '{kind}'.")
    except (NotFound, ValueError, IncompatibleRuns) as exc:
        return notice("error", str(exc))
    except KeyError as exc:
        return notice("error", f"Missing field {exc} in request.")
    except Exception as exc:  # keep the UI alive; details go to the log, not the screen
        log.exception("UI action %s failed", kind)
        return notice("error", f"Something went wrong ({type(exc).__name__}). See the server log for details.")
