"""Attribution heatmap generator formatting token weights for UI visualization."""

from __future__ import annotations

import re
from typing import List
from .attribution_schemas import AttributionHeatmapCell, AtomicClaim


def build_attribution_heatmap(text: str, claims: List[AtomicClaim]) -> List[AttributionHeatmapCell]:
    tokens = re.findall(r"\S+|\s+", text)
    cells: List[AttributionHeatmapCell] = []

    for t in tokens:
        matched_chunk = None
        weight = 0.0
        for c in claims:
            if t.strip() and t.strip().lower() in c.text.lower():
                matched_chunk = c.cited_chunk_id
                weight = c.entailment_score
                break

        cells.append(AttributionHeatmapCell(
            token=t,
            source_chunk_id=matched_chunk,
            confidence_weight=weight
        ))
    return cells
