"""Context compression and redundant passage filtering for token savings."""

from __future__ import annotations

import difflib
from typing import List
from .retrieval_schemas import ScoredPassage


class ContextCompressor:
    def __init__(self, similarity_threshold: float = 0.85):
        self.threshold = similarity_threshold

    def deduplicate(self, passages: List[ScoredPassage]) -> List[ScoredPassage]:
        """Removes near-duplicate passages based on text sequence similarity."""
        unique: List[ScoredPassage] = []
        for p in passages:
            is_dup = False
            for u in unique:
                ratio = difflib.SequenceMatcher(None, p.text, u.text).quick_ratio()
                if ratio >= self.threshold:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(p)
        return unique
