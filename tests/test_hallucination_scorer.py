"""Unit tests for hallucination rate calculation."""

from backend.hallucination_scorer import calculate_hallucination_index
from backend.attribution_schemas import AtomicClaim


def test_hallucination_index_critical():
    claims = [
        AtomicClaim(claim_id="1", text="a", char_start=0, char_end=1, is_supported=False),
        AtomicClaim(claim_id="2", text="b", char_start=2, char_end=3, is_supported=False),
    ]
    res = calculate_hallucination_index(claims)
    assert res["risk_level"] == "CRITICAL"
    assert res["hallucination_rate"] == 1.0
