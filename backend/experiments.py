"""Before/after comparison of two runs on the same test set."""

from __future__ import annotations

from typing import Any

from .schemas import EvaluationRun, QuestionResult

COMPARED_METRICS = [
    ("pass_rate", "Overall pass rate", None),
    ("hit_at_k", "Hit@k", "retriever"),
    ("context_recall", "Context recall", "retriever"),
    ("context_precision", "Context precision", "retriever"),
    ("answer_correctness", "Answer correctness (generator-only)", "generator"),
    ("faithfulness", "Faithfulness (end-to-end)", "end_to_end"),
    ("answer_correctness", "Answer correctness (end-to-end)", "end_to_end"),
    ("abstention_correct", "Abstention correctness", "end_to_end"),
]


class IncompatibleRuns(ValueError):
    pass


def _metric(run: EvaluationRun, key: str, mode: str | None) -> float | None:
    if mode is None:
        return run.summary.get(key)
    return run.summary.get("modes", {}).get(mode, {}).get("metrics", {}).get(key)


def compare_runs(
    baseline: EvaluationRun, candidate: EvaluationRun,
    baseline_results: list[QuestionResult], candidate_results: list[QuestionResult],
    strict: bool = True,
) -> dict[str, Any]:
    base_ids = {r.question_id for r in baseline_results}
    cand_ids = {r.question_id for r in candidate_results}
    warnings: list[str] = []
    if baseline.document_id != candidate.document_id:
        if strict:
            raise IncompatibleRuns("The runs evaluate different documents and cannot be compared fairly.")
        warnings.append("The runs evaluate different documents.")
    if base_ids != cand_ids:
        if strict:
            raise IncompatibleRuns("The runs use different question sets; re-run both on the same test set.")
        warnings.append("The runs use different question sets; only shared questions are compared.")

    base_cfg, cand_cfg = baseline.configuration.to_dict(), candidate.configuration.to_dict()
    changed = {k: {"baseline": base_cfg[k], "candidate": cand_cfg.get(k)} for k in base_cfg
               if k != "label" and base_cfg[k] != cand_cfg.get(k)}
    if len(changed) > 2:
        warnings.append(f"{len(changed)} settings changed at once; attributing the effect to one of them is hard.")
    if base_cfg.get("embedding_backend") != cand_cfg.get("embedding_backend"):
        warnings.append("The embedding backend differs between runs (one may have used the offline fallback).")
    shared = base_ids & cand_ids
    if len(shared) < 20:
        warnings.append(f"Only {len(shared)} questions: treat small differences as preliminary, not conclusive.")

    rows = []
    for key, label, mode in COMPARED_METRICS:
        b, c = _metric(baseline, key, mode), _metric(candidate, key, mode)
        delta = round(c - b, 4) if b is not None and c is not None else None
