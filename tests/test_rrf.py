"""Unit tests for Reciprocal Rank Fusion."""

from backend.rrf import reciprocal_rank_fusion


def test_rrf_scoring_order():
    dense = ["doc_a", "doc_b", "doc_c"]
    sparse = ["doc_b", "doc_a", "doc_d"]

    # doc_a: 1/(60+1) + 1/(60+2)
    # doc_b: 1/(60+2) + 1/(60+1)
    fused = reciprocal_rank_fusion(dense, sparse, k=60)
    top_two = [item[0] for item in fused[:2]]
    assert "doc_a" in top_two
    assert "doc_b" in top_two
    assert fused[-1][0] in ("doc_c", "doc_d")
