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

