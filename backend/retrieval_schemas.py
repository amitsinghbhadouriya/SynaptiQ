"""Data structures and configuration schemas for hybrid retrieval."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HybridSearchConfig(BaseModel):
    dense_weight: float = Field(0.6, ge=0.0, le=1.0, description="Weight for vector similarity")
    sparse_weight: float = Field(0.4, ge=0.0, le=1.0, description="Weight for BM25 lexical score")
    rrf_k: int = Field(60, ge=1, description="Reciprocal Rank Fusion constant factor")
    top_k: int = Field(5, ge=1, le=50, description="Final number of passages to return")
    use_reranker: bool = Field(False, description="Whether to apply cross-encoder reranking")


class ScoredPassage(BaseModel):
    chunk_id: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    dense_score: Optional[float] = None
    sparse_score: Optional[float] = None
    fused_score: float = 0.0
