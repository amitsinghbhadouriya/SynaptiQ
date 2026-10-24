import pytest

from backend.metrics import retrieval_metrics
from backend.schemas import Chunk, EvidenceSpan, RetrievedChunk
from backend.vector_store import collection_name


def test_retrieves_supporting_chunk(workspace, sample_bytes):
    document, created = workspace.ingest("handbook.txt", sample_bytes)
    assert created and document.metadata["chunk_count"] > 0
    config, embedder = workspace.resolve(workspace.default_config(top_k=3))
    hits = workspace._retriever(embedder).retrieve(document, config, "How many days of paid annual leave?", 3)
    assert hits and hits[0].rank == 1
    assert any("24 days of paid annual leave" in h.text for h in hits)


def test_duplicate_upload_is_reused(workspace, sample_bytes):
    first, created_first = workspace.ingest("a.txt", sample_bytes)
    second, created_second = workspace.ingest("b.txt", sample_bytes)
    assert created_first and not created_second
    assert first.document_id == second.document_id


def _chunk(i, start, end):
    return RetrievedChunk(chunk_id=f"c{i}", rank=i, score=1 - i / 10, text="", start_char=start, end_char=end)


def test_retrieval_metrics_hit_and_miss():
    evidence = [EvidenceSpan(100, 160, "x")]
    hit = retrieval_metrics(evidence, [_chunk(1, 90, 200), _chunk(2, 300, 400)], k=2)
