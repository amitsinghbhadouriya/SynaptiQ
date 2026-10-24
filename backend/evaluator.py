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
            metrics["ragas_string_similarity"] = ragas_adapter.string_similarity(result.answer, q.reference_answer)
        if result.input_tokens is not None:
            metrics["input_tokens"] = float(result.input_tokens)
            metrics["output_tokens"] = float(result.output_tokens or 0)
        return ModeResult(
            mode, passed, metrics=metrics, answer=result.answer, contexts=contexts,
            latency_ms=result.latency_ms, estimated_cost=result.estimated_cost,
        )

    # -------------------------------------------------------------- question
    def evaluate_question(self, document: Document, config: RunConfig, q: EvalQuestion, modes: list[str]) -> QuestionResult:
        results: dict[str, ModeResult] = {}
        retrieved: list[RetrievedChunk] = []
        if "retriever" in modes or "end_to_end" in modes or not q.answerable:
            retriever_result, retrieved = self._retriever_mode(document, config, q)
            if "retriever" in modes:
                results["retriever"] = retriever_result

        if "generator" in modes:
            evidence_contexts = [e.text for e in q.evidence] if q.answerable else [c.text for c in retrieved]
            results["generator"] = self._generate("generator", q, evidence_contexts, config)

        if "end_to_end" in modes:
            e2e = self._generate("end_to_end", q, [c.text for c in retrieved], config)
            if "retriever" not in modes:
                e2e.retrieved = retrieved
            # End-to-end latency covers retrieval plus generation.
            retrieval_latency = results.get("retriever").latency_ms if results.get("retriever") else 0
            if e2e.latency_ms is not None:
                e2e.latency_ms += retrieval_latency or 0
            results["end_to_end"] = e2e

        r = results.get("retriever")
        g = results.get("generator")
        e = results.get("end_to_end")
        notes: list[str] = []
        if r and r.metrics.get("hit_at_k") is not None:
            rank = r.metrics.get("first_relevant_rank")
            notes.append(
                f"Evidence {'found' if r.passed else 'missing'} in top-{config.top_k}"
                + (f" (first supporting chunk at rank {int(rank)})" if rank else " (not in the candidate list)")
                + f"; context recall {r.metrics.get('context_recall'):.2f}."
            )
        for label, mode in (("Generator-only", g), ("End-to-end", e)):
            if mode is None:
                continue
            if mode.error:
                notes.append(f"{label}: not measured ({mode.error}).")
                continue
            corr = mode.metrics.get("answer_correctness")
            faith = mode.metrics.get("faithfulness")
            parts = [f"{label}: {'pass' if mode.passed else 'fail'}"]
            if corr is not None:
                parts.append(f"correctness {corr:.2f}")
            if faith is not None:
                parts.append(f"faithfulness {faith:.2f}")
            if mode.metrics.get("abstained"):
                parts.append("declined to answer")
            notes.append(", ".join(parts) + ".")

        e2e_correct = None
        if e and e.metrics.get("answer_correctness") is not None:
            e2e_correct = e.metrics["answer_correctness"] >= M.CORRECTNESS_PASS
        diagnosis = diagnose(
            r.passed if r else None, g.passed if g else None, e.passed if e else None,
            answerable=q.answerable, end_to_end_correct=e2e_correct, notes=notes,
        )
        result = QuestionResult(
            question_id=q.question_id, modes=results, diagnosis=diagnosis.code, diagnosis_label=diagnosis.label,
            diagnosis_reason=diagnosis.reason + " Next: " + diagnosis.next_action, evidence_notes=diagnosis.evidence,
        )
        result.recommendation = for_question(result, config) if diagnosis.code != "PASS" else None
        return result
