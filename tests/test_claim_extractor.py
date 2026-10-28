"""Unit tests for atomic claim extraction."""

from backend.claim_extractor import ClaimExtractor


def test_claim_extractor_segmentation():
    extractor = ClaimExtractor()
    text = "SynaptiQ is an evaluation tool. It detects hallucinations accurately!"
    claims = extractor.extract_claims(text)
    assert len(claims) == 2
    assert "SynaptiQ is an evaluation tool." in claims[0].text
    assert "It detects hallucinations accurately!" in claims[1].text
