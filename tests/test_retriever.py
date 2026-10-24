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
    assert hit["hit_at_k"] == 1.0 and hit["context_recall"] == 1.0 and hit["mrr"] == 1.0
    miss = retrieval_metrics(evidence, [_chunk(1, 300, 400), _chunk(2, 500, 600), _chunk(3, 95, 170)], k=2)
    assert miss["hit_at_k"] == 0.0 and miss["context_recall"] == 0.0
    assert miss["first_relevant_rank"] == 3.0 and miss["full_coverage_rank"] == 3.0


def test_multi_span_needs_all_evidence():
    evidence = [EvidenceSpan(0, 50, "a"), EvidenceSpan(500, 550, "b")]
    metrics = retrieval_metrics(evidence, [_chunk(1, 0, 100), _chunk(2, 480, 600)], k=1)
    assert metrics["hit_at_k"] == 0.0 and metrics["context_recall"] == 0.5
    assert metrics["full_coverage_rank"] == 2.0


def test_unanswerable_has_no_retrieval_score():
    assert retrieval_metrics([], [_chunk(1, 0, 10)], k=1)["hit_at_k"] is None


def test_chroma_store_roundtrip(tmp_path):
    pytest.importorskip("chromadb")
    from backend.vector_store import ChromaVectorStore

    store = ChromaVectorStore(tmp_path / "chroma")
    name = collection_name("doc_x", "abc123")
    chunks = [Chunk(f"doc_x-abc123-{i:04d}", "doc_x", i, f"text {i}", i * 10, i * 10 + 5, "abc123") for i in range(3)]
    vectors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    store.upsert(name, chunks, vectors)
    assert store.has_collection(name, 3)
    top = store.query(name, [0.0, 0.9, 0.1], 2)
    assert top[0][0] == "doc_x-abc123-0001"
    store.delete_prefix("sq-doc_x-")
    assert not store.has_collection(name, 3)
