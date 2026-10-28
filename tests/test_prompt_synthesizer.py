"""Unit tests for prompt synthesizer."""

from backend.prompt_synthesizer import PromptSynthesizer


def test_synthesize_factual():
    pair = PromptSynthesizer.synthesize_factual("chunk_1", "Revenue increased by 28% in 2025.")
    assert "Revenue increased" in pair.question
    assert pair.question_type == "factual"
