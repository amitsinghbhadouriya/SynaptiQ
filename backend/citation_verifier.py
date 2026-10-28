"""Verifies inline citations against retrieved context passages."""

from __future__ import annotations

from typing import List, Dict
from .attribution_schemas import AtomicClaim
from .entailment_checker import EntailmentChecker


class CitationVerifier:
    def verify_citations(
        self,
        claims: List[AtomicClaim],
        passages: Dict[str, str]
    ) -> List[AtomicClaim]:
        for claim in claims:
            best_chunk = None
            best_score = 0.0
            for chunk_id, text in passages.items():
                supported, score = EntailmentChecker.verify_support(text, claim.text)
                if score > best_score:
                    best_score = score
                    best_chunk = chunk_id

            claim.cited_chunk_id = best_chunk
            claim.entailment_score = best_score
            claim.is_supported = best_score >= 0.5
        return claims
