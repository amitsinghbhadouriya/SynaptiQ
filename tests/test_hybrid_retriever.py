"""Unit tests for HybridRetriever coordinator."""

from backend.hybrid_retriever import HybridRetriever
from backend.retrieval_schemas import HybridSearchConfig


def test_hybrid_retriever_fuse():
    retriever = HybridRetriever(HybridSearchConfig(top_k=2))
    dense = [{"id": "c1", "text": "hello world"}, {"id": "c2", "text": "another chunk"}]
    sparse = [{"id": "c2", "text": "another chunk"}, {"id": "c3", "text": "third chunk"}]

    fused = retriever.fuse(dense, sparse)
    assert len(fused) == 2
    assert fused[0].chunk_id == "c2"
