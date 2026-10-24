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
