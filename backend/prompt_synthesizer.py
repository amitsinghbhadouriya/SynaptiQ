"""Prompt synthesizer constructing tailored evaluation questions from source context."""

from __future__ import annotations

from typing import List
from .qa_schemas import GeneratedQAPair


class PromptSynthesizer:
    @staticmethod
    def synthesize_factual(chunk_id: str, chunk_text: str) -> GeneratedQAPair:
        snippet = chunk_text[:80].strip()
        return GeneratedQAPair(
            question_id=f"q_{chunk_id}_fact",
            question=f"What key information is described regarding: {snippet}?",
            expected_answer=chunk_text[:150],
            source_chunk_id=chunk_id,
            question_type="factual"
        )

    @staticmethod
    def batch_synthesize(chunks: List[dict]) -> List[GeneratedQAPair]:
        """Processes chunks in batch for rapid dataset generation."""
        return [
            PromptSynthesizer.synthesize_factual(c["id"], c.get("text", ""))
            for c in chunks
        ]
