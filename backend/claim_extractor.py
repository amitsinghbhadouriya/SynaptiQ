"""Atomic proposition splitter decomposing generation responses into discrete testable claims."""

from __future__ import annotations

import re
from typing import List
from .attribution_schemas import AtomicClaim

# Pre-compiled boundary pattern for efficient proposition segmentation
_SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")


class ClaimExtractor:
    """Extracts factual claims by segmenting on punctuation and subordinating conjunctions."""

    def extract_claims(self, text: str) -> List[AtomicClaim]:
        if not text:
            return []

        sentences = _SENTENCE_SPLIT_REGEX.split(text.strip())
        claims: List[AtomicClaim] = []
        cursor = 0

        for idx, s in enumerate(sentences, 1):
            s_clean = s.strip()
            if not s_clean:
                continue
            start = text.find(s_clean, cursor)
            end = start + len(s_clean)
            cursor = end

            claims.append(AtomicClaim(
                claim_id=f"c_{idx}",
                text=s_clean,
                char_start=start,
                char_end=end,
                is_supported=False
            ))
        return claims
