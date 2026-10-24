"""Optional Ragas metrics.

Uses Ragas metrics that need no LLM judge, so they run offline:

* ragas_context_recall  — Ragas non-LLM context recall. Retrieved chunks are split into
  sentences first so a one-sentence evidence passage is compared like-for-like.
* ragas_string_similarity — Ragas NonLLMStringSimilarity between answer and reference.

Ragas APIs change between releases; every call is guarded and returns None on failure
(recorded as "unavailable", never as zero). Verified against ragas 0.4.3.
"""

from __future__ import annotations

import logging
import warnings
from functools import lru_cache

from .text_utils import split_sentences

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load() -> dict:
    state: dict = {"available": False, "version": None, "error": None}
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import ragas
            from ragas import SingleTurnSample

            try:
                from ragas.metrics import _NonLLMContextRecall as ContextRecall
            except ImportError:  # older releases expose the public name
                from ragas.metrics import NonLLMContextRecall as ContextRecall
            try:
                from ragas.metrics.collections import NonLLMStringSimilarity
            except ImportError:
                from ragas.metrics import NonLLMStringSimilarity
        state.update(
            available=True, version=getattr(ragas, "__version__", "unknown"), sample=SingleTurnSample,
            recall=ContextRecall(), similarity=NonLLMStringSimilarity(),
        )
    except Exception as exc:
        state["error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
        log.info("Ragas metrics unavailable: %s", state["error"])
    return state


def status(enabled: bool = True) -> dict:
    if not enabled:
        return {"available": False, "version": None, "error": "disabled by RAGAS_ENABLED=false"}
    state = _load()
    return {"available": state["available"], "version": state["version"], "error": state["error"]}


def context_recall(retrieved_texts: list[str], evidence_texts: list[str]) -> float | None:
    state = _load()
    if not state["available"] or not evidence_texts:
        return None
    sentences = [s.text for text in retrieved_texts for s in split_sentences(text)] or [""]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sample = state["sample"](retrieved_contexts=sentences, reference_contexts=evidence_texts)
            value = state["recall"].single_turn_score(sample)
        return round(float(value), 4)
    except Exception as exc:
        log.debug("ragas context recall failed: %s", exc)
        return None


def string_similarity(answer: str | None, reference: str | None) -> float | None:
    state = _load()
    if not state["available"] or not answer or not reference:
        return None
    metric = state["similarity"]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if hasattr(metric, "score") and not hasattr(metric, "single_turn_score"):
                value = metric.score(reference=reference, response=answer)
                value = getattr(value, "value", value)
            else:
                value = metric.single_turn_score(state["sample"](response=answer, reference=reference))
        return round(float(value), 4)
    except Exception as exc:
        log.debug("ragas string similarity failed: %s", exc)
        return None
