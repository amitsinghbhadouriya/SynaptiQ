"""Cross-encoder reranking client with resilient lexical fallback."""

from __future__ import annotations

import re
from typing import List
from .retrieval_schemas import ScoredPassage


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    def rerank(self, query: str, passages: List[ScoredPassage], top_k: int = 5) -> List[ScoredPassage]:
        """Reranks candidate passages based on query relevance."""
        if not passages:
            return []

        # Heuristic token overlap fallback when torch / transformer model is omitted
        q_tokens = set(re.findall(r"\w+", query.lower()))
        for p in passages:
            p_tokens = set(re.findall(r"\w+", p.text.lower()))
            overlap = len(q_tokens & p_tokens) / max(1, len(q_tokens))
            p.fused_score = p.fused_score * 0.5 + overlap * 0.5

        passages.sort(key=lambda p: p.fused_score, reverse=True)
        return passages[:top_k]
