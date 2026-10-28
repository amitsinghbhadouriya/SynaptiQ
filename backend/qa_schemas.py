"""Configuration models and typologies for synthetic QA dataset generation."""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class QAGenerationConfig(BaseModel):
    num_questions_per_chunk: int = Field(2, ge=1, le=10)
    difficulty: str = Field("medium", pattern="^(easy|medium|hard)$")
    include_negative_samples: bool = Field(True)
    question_types: List[str] = Field(default_factory=lambda: ["factual", "inferential", "summary"])


class GeneratedQAPair(BaseModel):
    question_id: str
    question: str
    expected_answer: str
    source_chunk_id: str
    question_type: str = "factual"
    is_hard_negative: bool = False
