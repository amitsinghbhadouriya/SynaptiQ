"""Turn diagnoses into concrete, testable configuration changes.

A recommendation is a hypothesis to verify with a before/after run on the same test
set — never a guaranteed fix.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .schemas import QuestionResult, RunConfig

STRONGER_EMBEDDINGS = {
    "sentence-transformers/all-MiniLM-L6-v2": "sentence-transformers/all-mpnet-base-v2",
}


def _change(key: str, value: Any, config: RunConfig) -> dict[str, Any]:
    return {"key": key, "from": getattr(config, key), "to": value}


def for_question(result: QuestionResult, config: RunConfig) -> dict[str, Any] | None:
    """Suggest one change for a failing question, using its measured evidence."""
    code = result.diagnosis
    retriever = result.modes.get("retriever")
    metrics = retriever.metrics if retriever else {}
    first_rank = metrics.get("first_relevant_rank")
    full_rank = metrics.get("full_coverage_rank")
    recall = metrics.get("context_recall") or 0.0

    if code in {"LIKELY_RETRIEVAL_FAILURE", "LIKELY_COMBINED_FAILURE", "CORRECT_BUT_UNGROUNDED"}:
        if full_rank and config.top_k < full_rank <= 10:
            new_k = int(full_rank)
            why = (f"The supporting chunk was ranked #{int(first_rank)}, outside the top {config.top_k}."
                   if first_rank and first_rank > config.top_k else
                   f"Only part of the evidence was in the top {config.top_k}; all of it is covered by the top {new_k}.")
            return {
                "title": f"Increase top-k from {config.top_k} to {new_k}",
                "why": why,
                "change": _change("top_k", new_k, config),
            }
        if 0 < recall < 0.5 or config.chunk_overlap < 50:
            new_size = min(2000, int(config.chunk_size * 1.6 // 50 * 50))
            return {
                "title": f"Use larger, overlapping chunks ({new_size}/{max(config.chunk_overlap, new_size // 6)})",
                "why": "The evidence is only partly covered — it is likely split across chunk boundaries.",
                "change": {**_change("chunk_size", new_size, config),
                           "also": {"chunk_overlap": max(config.chunk_overlap, new_size // 6)}},
            }
        stronger = STRONGER_EMBEDDINGS.get(config.embedding_model)
        if stronger:
            return {
                "title": "Try a stronger embedding model",
                "why": "The evidence never appears near the top; the embedding may not capture this vocabulary.",
                "change": _change("embedding_model", stronger, config),
            }
        return {
            "title": f"Increase top-k from {config.top_k} to {min(20, config.top_k + 4)}",
            "why": "The evidence is not retrieved; a wider candidate set is the cheapest next test.",
            "change": _change("top_k", min(20, config.top_k + 4), config),
        }
    if code == "LIKELY_GENERATION_FAILURE":
        answer = (result.modes.get("generator") or result.modes.get("end_to_end"))
        abstained = bool(answer and answer.metrics.get("abstained"))
        should_abstain = bool(answer and answer.metrics.get("abstention_correct") == 0.0 and not abstained
                              and answer.metrics.get("answer_correctness") is None)
        if should_abstain:
            if config.llm_provider == "offline":
                new_threshold = round(min(0.9, config.abstain_threshold + 0.1), 2)
                return {
                    "title": f"Raise the abstention threshold to {new_threshold}",
                    "why": "The question is not answerable from the document, yet the generator answered from "
                           "loosely related text.",
                    "change": _change("abstain_threshold", new_threshold, config),
                }
            return {
                "title": "Switch to the strict grounded prompt",
                "why": "The model answered a question the evidence cannot support instead of declining.",
                "change": _change("prompt_version", "grounded-strict-v2", config),
            }
        if abstained and config.llm_provider == "offline":
            new_threshold = round(max(0.1, config.abstain_threshold - 0.1), 2)
            return {
                "title": f"Lower the abstention threshold to {new_threshold}",
                "why": "The generator declined although the evidence contained the answer.",
                "change": _change("abstain_threshold", new_threshold, config),
            }
        if config.llm_provider == "offline":
            return {
                "title": "Answer with a single best sentence",
                "why": "Extra sentences diluted or contradicted the supported answer.",
                "change": _change("max_answer_sentences", 1, config),
            }
        return {
            "title": "Switch to the strict grounded prompt",
            "why": "The model added claims that are not in the evidence or answered without support.",
            "change": _change("prompt_version", "grounded-strict-v2", config),
