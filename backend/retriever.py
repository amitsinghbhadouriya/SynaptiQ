"""Index building and top-k retrieval over one document's chunks."""

from __future__ import annotations

import threading

from .chunking import chunk_document
from .embeddings import Embedder
from .schemas import Chunk, Document, RetrievedChunk, RunConfig
from .storage import Storage
from .vector_store import VectorStore, collection_name


class Retriever:
    def __init__(self, storage: Storage, store: VectorStore, embedder: Embedder):
        self.storage = storage
        self.store = store
        self.embedder = embedder
        self._chunk_cache: dict[tuple[str, str], dict[str, Chunk]] = {}
        self._lock = threading.Lock()

    def ensure_index(self, document: Document, config: RunConfig) -> list[Chunk]:
        """Chunk + embed + index the document for these settings (reused if already built)."""
        key = config.index_key
        with self._lock:
            chunks = self.storage.get_chunks(document.document_id, key)
            if not chunks:
                chunks = chunk_document(document, config.chunk_size, config.chunk_overlap, key)
                self.storage.save_chunks(chunks)
            name = collection_name(document.document_id, key)
            if not self.store.has_collection(name, len(chunks)):
                self.store.upsert(name, chunks, self.embedder.embed([c.text for c in chunks]))
            self._chunk_cache[(document.document_id, key)] = {c.chunk_id: c for c in chunks}
        return chunks

    def retrieve(self, document: Document, config: RunConfig, question: str, k: int) -> list[RetrievedChunk]:
        key = config.index_key
        lookup = self._chunk_cache.get((document.document_id, key))
        if lookup is None:
            lookup = {c.chunk_id: c for c in self.ensure_index(document, config)}
        vector = self.embedder.embed([question])[0]
        hits = self.store.query(collection_name(document.document_id, key), vector, k)
        results = []
        for rank, (chunk_id, score) in enumerate(hits, start=1):
            chunk = lookup.get(chunk_id)
            if chunk is None:
                continue
            results.append(RetrievedChunk(
                chunk_id=chunk_id, rank=rank, score=round(float(score), 4), text=chunk.text,
                start_char=chunk.start_char, end_char=chunk.end_char, page_number=chunk.page_number,
            ))
        return results
