"""Unit tests for CrossEncoderReranker fallback."""

from backend.reranker import CrossEncoderReranker
from backend.retrieval_schemas import ScoredPassage


def test_reranker_lexical_overlap():
    reranker = CrossEncoderReranker()
    p1 = ScoredPassage(chunk_id="1", text="Python programming guide", fused_score=0.1)
    p2 = ScoredPassage(chunk_id="2", text="Irrelevant content about apples", fused_score=0.2)

    results = reranker.rerank("Python programming", [p1, p2], top_k=2)
    assert results[0].chunk_id == "1"
