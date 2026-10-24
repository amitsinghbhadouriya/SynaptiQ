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
