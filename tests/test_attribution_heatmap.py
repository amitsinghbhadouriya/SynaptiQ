"""Unit tests for attribution heatmap generation."""

from backend.attribution_heatmap import build_attribution_heatmap
from backend.attribution_schemas import AtomicClaim


def test_build_attribution_heatmap():
    claims = [AtomicClaim(claim_id="1", text="FastAPI server", char_start=0, char_end=14, cited_chunk_id="chunk_a", entailment_score=0.9)]
    cells = build_attribution_heatmap("FastAPI server", claims)
    assert len(cells) > 0
    assert cells[0].source_chunk_id == "chunk_a"
