"""Results tables (pandas) and CSV/JSON exports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .schemas import EvalQuestion, EvaluationRun, QuestionResult, to_jsonable


def results_frame(results: list[QuestionResult], questions: list[EvalQuestion]) -> pd.DataFrame:
    """One row per question with the headline metric of each mode and the diagnosis."""
    by_id = {q.question_id: q for q in questions}
    rows = []
    for r in results:
        q = by_id.get(r.question_id)
        ret, gen, e2e = r.modes.get("retriever"), r.modes.get("generator"), r.modes.get("end_to_end")
        rows.append({
            "question_id": r.question_id,
            "question": q.question if q else "",
            "type": q.question_type if q else "",
            "reference_answer": q.reference_answer if q else "",
            "retriever_pass": ret.passed if ret else None,
            "hit_at_k": ret.metrics.get("hit_at_k") if ret else None,
            "context_recall": ret.metrics.get("context_recall") if ret else None,
            "context_precision": ret.metrics.get("context_precision") if ret else None,
            "first_relevant_rank": ret.metrics.get("first_relevant_rank") if ret else None,
            "generator_pass": gen.passed if gen else None,
            "generator_correctness": gen.metrics.get("answer_correctness") if gen else None,
            "end_to_end_pass": e2e.passed if e2e else None,
            "e2e_correctness": e2e.metrics.get("answer_correctness") if e2e else None,
            "faithfulness": e2e.metrics.get("faithfulness") if e2e else None,
            "answer_relevancy": e2e.metrics.get("answer_relevancy") if e2e else None,
            "abstained": e2e.metrics.get("abstained") if e2e else None,
            "ragas_context_recall": ret.metrics.get("ragas_context_recall") if ret else None,
            "ragas_string_similarity": e2e.metrics.get("ragas_string_similarity") if e2e else None,
            "generated_answer": e2e.answer if e2e else None,
            "diagnosis": r.diagnosis_label,
            "diagnosis_code": r.diagnosis,
            "diagnosis_reason": r.diagnosis_reason,
            "recommendation": r.recommendation["title"] if r.recommendation else "",
            "latency_ms": e2e.latency_ms if e2e else (ret.latency_ms if ret else None),
            "estimated_cost": e2e.estimated_cost if e2e else None,
        })
    return pd.DataFrame(rows)


def runs_frame(runs: list[EvaluationRun]) -> pd.DataFrame:
    rows = []
    for run in runs:
        h = run.summary.get("headline", {})
        rows.append({
            "run_id": run.run_id, "label": run.label, "created_at": run.created_at, "status": run.status,
            "questions": run.summary.get("questions"), "pass_rate": run.summary.get("pass_rate"),
            "hit_at_k": h.get("hit_at_k"), "context_recall": h.get("context_recall"),
            "faithfulness": h.get("faithfulness"), "answer_correctness": h.get("answer_correctness"),
            "latency_ms_avg": h.get("latency_ms_avg"), "config": run.configuration.short(),
            "duration_ms": run.duration_ms,
        })
    return pd.DataFrame(rows)


def export_run(run: EvaluationRun, results: list[QuestionResult], questions: list[EvalQuestion], fmt: str,
               out_dir: Path | None = None) -> tuple[str, str, str]:
    """Return (filename, mime, content) and optionally write the file to out_dir."""
    fmt = fmt.lower()
    if fmt == "csv":
        content = results_frame(results, questions).to_csv(index=False)
        filename, mime = f"synaptiq_{run.run_id}.csv", "text/csv"
    elif fmt == "json":
        payload: dict[str, Any] = {
            "run": run.to_dict(),
            "questions": [q.to_dict() for q in questions],
            "results": to_jsonable(results),
        }
        content = json.dumps(payload, indent=2, ensure_ascii=False)
        filename, mime = f"synaptiq_{run.run_id}.json", "application/json"
    else:
        raise ValueError("Supported export formats are csv and json.")
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / filename).write_text(content, encoding="utf-8")
    return filename, mime, content
