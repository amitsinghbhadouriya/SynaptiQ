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
