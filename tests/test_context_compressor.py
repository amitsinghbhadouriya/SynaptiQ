"""Unit tests for context compression."""

from backend.context_compressor import ContextCompressor
from backend.retrieval_schemas import ScoredPassage


def test_context_compressor_deduplication():
    compressor = ContextCompressor(similarity_threshold=0.8)
    p1 = ScoredPassage(chunk_id="1", text="The quick brown fox jumps over the lazy dog.")
    p2 = ScoredPassage(chunk_id="2", text="The quick brown fox jumps over the lazy dog!")
    p3 = ScoredPassage(chunk_id="3", text="Completely distinct sentence about robotics.")

    unique = compressor.deduplicate([p1, p2, p3])
    assert len(unique) == 2
    assert unique[0].chunk_id == "1"
    assert unique[1].chunk_id == "3"
