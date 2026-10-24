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


