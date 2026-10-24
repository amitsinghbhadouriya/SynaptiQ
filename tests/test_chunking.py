import pytest

from backend.chunking import chunk_document
from backend.document_loader import load_document
from backend.schemas import Document


@pytest.fixture
def document(sample_bytes):
    loaded = load_document("handbook.txt", sample_bytes)
    return Document(
        document_id="doc_test", filename=loaded.filename, file_type=loaded.file_type,
        content_hash=loaded.content_hash, text=loaded.text, metadata=loaded.metadata,
    )


def test_chunks_respect_size_and_offsets(document):
    chunks = chunk_document(document, 300, 60, "k1")
    assert chunks
    for chunk in chunks:
        assert len(chunk.text) <= 300
        assert document.text[chunk.start_char : chunk.end_char] == chunk.text


def test_chunk_ids_are_stable(document):
    first = [c.chunk_id for c in chunk_document(document, 300, 60, "k1")]
    second = [c.chunk_id for c in chunk_document(document, 300, 60, "k1")]
    assert first == second
    assert len(set(first)) == len(first)


def test_overlap_repeats_trailing_text(document):
    chunks = chunk_document(document, 300, 120, "k2")
    overlapping = sum(1 for a, b in zip(chunks, chunks[1:]) if b.start_char < a.end_char)
    assert overlapping > 0


def test_chunks_never_cross_sections(document):
    sections = document.sections
    for chunk in chunk_document(document, 500, 80, "k3"):
        assert any(s.start <= chunk.start_char and chunk.end_char <= s.end for s in sections)


def test_invalid_settings():
    doc = Document("d", "x.txt", "TXT", "h", "Some text here.")
    with pytest.raises(ValueError):
        chunk_document(doc, 20, 0, "k")
    with pytest.raises(ValueError):
        chunk_document(doc, 200, 200, "k")
