"""Unit tests for citation verification."""

from backend.citation_verifier import CitationVerifier
from backend.attribution_schemas import AtomicClaim


def test_citation_verifier_matching():
    verifier = CitationVerifier()
    claims = [
        AtomicClaim(claim_id="1", text="ChromaDB uses HNSW", char_start=0, char_end=18)
    ]
    passages = {"chunk_1": "ChromaDB vector store uses HNSW indexing for rapid lookups."}

    verified = verifier.verify_citations(claims, passages)
    assert verified[0].cited_chunk_id == "chunk_1"
    assert verified[0].is_supported is True
