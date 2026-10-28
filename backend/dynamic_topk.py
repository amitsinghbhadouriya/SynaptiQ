"""Dynamic top-k selection adapting context length to retrieval score distribution."""

from __future__ import annotations

from typing import List
from .retrieval_schemas import ScoredPassage


def select_dynamic_topk(
    passages: List[ScoredPassage],
    min_k: int = 2,
    max_k: int = 8,
    decay_cutoff: float = 0.4
) -> List[ScoredPassage]:
    """Selects top passages dynamically before relative confidence drops significantly."""
    if len(passages) <= min_k:
        return passages

    top_score = max(p.fused_score for p in passages) if passages else 1.0
    selected = []

    for idx, p in enumerate(passages):
        if idx < min_k:
            selected.append(p)
        elif idx < max_k and (p.fused_score / max(1e-6, top_score)) >= decay_cutoff:
            selected.append(p)
        else:
            break

    return selected
