"""Vector index backed by ChromaDB, with an in-memory fallback.

One collection per (document, index settings) pair. Embeddings are computed by
SynaptiQ and passed in explicitly, so Chroma never downloads its own model.
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Protocol

from .embeddings import cosine
from .schemas import Chunk

log = logging.getLogger(__name__)


class VectorStore(Protocol):
    backend: str

    def has_collection(self, name: str, expected_count: int) -> bool: ...

    def upsert(self, name: str, chunks: list[Chunk], embeddings: list[list[float]]) -> None: ...

    def query(self, name: str, embedding: list[float], k: int) -> list[tuple[str, float]]: ...

    def delete_prefix(self, prefix: str) -> None: ...


def collection_name(document_id: str, index_key: str) -> str:
    # Chroma names: 3-63 chars of [a-zA-Z0-9._-], starting and ending alphanumeric.
    return f"sq-{document_id}-{index_key}"[:63]


class MemoryVectorStore:
    backend = "memory"

    def __init__(self):
        self._data: dict[str, dict[str, list[float]]] = {}
        self._lock = threading.Lock()

    def has_collection(self, name: str, expected_count: int) -> bool:
        return len(self._data.get(name, {})) == expected_count > 0

    def upsert(self, name: str, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        with self._lock:
            bucket = self._data.setdefault(name, {})
            for chunk, vector in zip(chunks, embeddings):
                bucket[chunk.chunk_id] = vector

    def query(self, name: str, embedding: list[float], k: int) -> list[tuple[str, float]]:
        bucket = self._data.get(name, {})
        scored = [(chunk_id, cosine(embedding, vector)) for chunk_id, vector in bucket.items()]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:k]

    def delete_prefix(self, prefix: str) -> None:
        with self._lock:
            for name in [n for n in self._data if n.startswith(prefix)]:
                del self._data[name]


class ChromaVectorStore:
    backend = "chroma"

    def __init__(self, path: Path):
        import chromadb
        from chromadb.config import Settings as ChromaSettings

        path.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(path), settings=ChromaSettings(anonymized_telemetry=False))
        self._lock = threading.Lock()

    def _collection(self, name: str):
        return self._client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"}, embedding_function=None)

    def has_collection(self, name: str, expected_count: int) -> bool:
        try:
            return self._client.get_collection(name=name, embedding_function=None).count() == expected_count > 0
        except Exception:
            return False

    def upsert(self, name: str, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        with self._lock:
            collection = self._collection(name)
            batch = 256
            for i in range(0, len(chunks), batch):
                part = chunks[i : i + batch]
                collection.upsert(
                    ids=[c.chunk_id for c in part],
                    embeddings=embeddings[i : i + batch],
                    documents=[c.text for c in part],
                    metadatas=[
                        {
                            "document_id": c.document_id,
                            "chunk_index": c.chunk_index,
                            "start_char": c.start_char,
                            "end_char": c.end_char,
                            "page_number": c.page_number if c.page_number is not None else -1,
                            "section": str(c.metadata.get("section", "")),
                        }
                        for c in part
                    ],
                )

    def query(self, name: str, embedding: list[float], k: int) -> list[tuple[str, float]]:
        collection = self._collection(name)
        count = collection.count()
        if count == 0:
            return []
        result = collection.query(query_embeddings=[embedding], n_results=min(k, count), include=["distances"])
        ids = result.get("ids", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [(chunk_id, 1.0 - float(distance)) for chunk_id, distance in zip(ids, distances)]

    def delete_prefix(self, prefix: str) -> None:
        with self._lock:
            for collection in self._client.list_collections():
                name = collection if isinstance(collection, str) else collection.name
                if name.startswith(prefix):
                    self._client.delete_collection(name)


def create_vector_store(backend: str, chroma_path: Path) -> tuple[VectorStore, str | None]:
    """Return (store, fallback_reason)."""
    backend = (backend or "auto").lower()
    if backend == "memory":
        return MemoryVectorStore(), None
    try:
        return ChromaVectorStore(chroma_path), None
    except Exception as exc:
        if backend == "chroma":
            raise
        reason = f"{type(exc).__name__}: {str(exc)[:160]}"
        log.warning("ChromaDB unavailable, using in-memory vectors (%s)", reason)
        return MemoryVectorStore(), reason
