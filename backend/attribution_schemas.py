"""Data models for fine-grained claim extraction and source attribution."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AtomicClaim(BaseModel):
    claim_id: str
    text: str
    char_start: int
    char_end: int
    entailment_score: float = 0.0
    cited_chunk_id: Optional[str] = None
    is_supported: bool = False


class AttributionHeatmapCell(BaseModel):
    token: str
    source_chunk_id: Optional[str] = None
    confidence_weight: float = 0.0
