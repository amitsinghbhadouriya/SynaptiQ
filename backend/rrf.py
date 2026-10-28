"""Reciprocal Rank Fusion (RRF) combining dense and lexical ranking signals."""

from __future__ import annotations

from typing import List, Dict, Tuple


def reciprocal_rank_fusion(
    dense_ranks: List[str],
    sparse_ranks: List[str],
    k: int = 60,
    dense_weight: float = 1.0,
    sparse_weight: float = 1.0
) -> List[Tuple[str, float]]:
    """Merges two ranked lists of chunk IDs using weighted Reciprocal Rank Fusion."""
    scores: Dict[str, float] = {}

    for rank, chunk_id in enumerate(dense_ranks, start=1):
        scores[chunk_id] = scores.get(chunk_id, 0.0) + dense_weight * (1.0 / (k + rank))

    for rank, chunk_id in enumerate(sparse_ranks, start=1):
        scores[chunk_id] = scores.get(chunk_id, 0.0) + sparse_weight * (1.0 / (k + rank))

    sorted_results = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_results
