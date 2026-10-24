"""Evaluation orchestrator: retriever-only, generator-only and end-to-end tests.

* Retriever-only: the question goes to the retriever; returned chunks are compared with
  the labeled evidence spans. Generation is not involved.
* Generator-only: the generator gets the question plus the known-correct evidence,
  bypassing the retriever. (Unanswerable questions get the top retrieved chunks as
  distractors, since no correct evidence exists; the expected behaviour is to decline.)
* End-to-end: normal retrieval followed by generation over the retrieved chunks.

Each mode is scored independently, then combined into a diagnosis and a suggestion.
"""

from __future__ import annotations

import time
from typing import Callable

from . import metrics as M
from . import ragas_adapter
from .embeddings import Embedder
from .generator import Generator
from .recommendations import for_question, top_recommendation
from .retriever import Retriever
from .root_cause import diagnose
from .schemas import (
    MODES,
    Document,
    EvalQuestion,
    ModeResult,
    QuestionResult,
    RetrievedChunk,
    RunConfig,
)

ProgressFn = Callable[[int, int, str], None]


class Evaluator:
    def __init__(self, retriever: Retriever, generator: Generator, embedder: Embedder, ragas_enabled: bool = True):
        self.retriever = retriever
        self.generator = generator
        self.embedder = embedder
        self.ragas_enabled = ragas_enabled and ragas_adapter.status(True)["available"]

    # ------------------------------------------------------------------ modes
    def _retriever_mode(self, document: Document, config: RunConfig, q: EvalQuestion) -> tuple[ModeResult, list[RetrievedChunk]]:
        started = time.perf_counter()
        try:
            # Fetch extra candidates to learn *where* the evidence ranked; only top-k is scored.
            candidates = self.retriever.retrieve(document, config, q.question, max(config.top_k * 3, config.top_k + 5))
        except Exception as exc:
            return ModeResult("retriever", None, error=f"Retrieval failed: {type(exc).__name__}"), []
        latency = int((time.perf_counter() - started) * 1000)
        top = candidates[: config.top_k]
        if q.answerable:
            metrics = M.retrieval_metrics(q.evidence, candidates, config.top_k)
            if self.ragas_enabled:
                metrics["ragas_context_recall"] = ragas_adapter.context_recall(
                    [c.text for c in top], [e.text for e in q.evidence]
                )
            passed = None if metrics["hit_at_k"] is None else metrics["hit_at_k"] == 1.0
        else:
            metrics, passed = {"top_score": top[0].score if top else None}, None
        return ModeResult("retriever", passed, metrics=metrics, retrieved=top, latency_ms=latency), top

    def _generate(self, mode: str, q: EvalQuestion, contexts: list[str], config: RunConfig) -> ModeResult:
        result = self.generator.generate(q.question, contexts, config)
        if result.error:
            return ModeResult(mode, None, contexts=contexts, latency_ms=result.latency_ms, error=result.error)
        metrics, passed = M.generation_metrics(
            q.question, result.answer, q.reference_answer, contexts, q.answerable, self.embedder
        )
        if self.ragas_enabled and q.answerable:
