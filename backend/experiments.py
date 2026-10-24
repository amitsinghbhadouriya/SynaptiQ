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
