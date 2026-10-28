"""Unit tests for hallucination mitigations."""

from backend.hallucination_mitigation import generate_hallucination_mitigations


def test_mitigations_critical():
    m = generate_hallucination_mitigations("CRITICAL", 3)
    assert any("temperature" in x.lower() for x in m)
