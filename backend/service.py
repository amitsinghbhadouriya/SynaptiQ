"""High-level workspace API shared by the Streamlit app and the FastAPI service."""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Any, Callable

from . import process_lock, ragas_adapter
from .config import Settings, load_settings
from .document_loader import load_document
from .embeddings import Embedder, get_embedder
from .evaluator import Evaluator, ProgressFn
from .experiments import compare_runs
from .generator import create_generator
from .reports import export_run
from .retriever import Retriever
from .schemas import MODES, Document, EvalQuestion, EvaluationRun, RunConfig, new_id, utc_now
from .storage import Storage
from .synthetic_qa import generate_offline, generate_with_llm, import_questions, load_curated_set, supporting_chunk_ids
from .vector_store import create_vector_store

log = logging.getLogger(__name__)

DEMO_DOCUMENT = "lumen_labs_handbook.txt"
DEMO_TEST_SET = "lumen_labs_handbook.json"
# A deliberately narrow baseline (small chunks, one retrieved chunk) so the demo has a
# reproducible retrieval failure to diagnose; the recommended candidate is then measured for real.
DEMO_BASELINE = {"chunk_size": 280, "chunk_overlap": 0, "top_k": 1, "label": "Baseline (demo)"}


class NotFound(LookupError):
    pass


class Workspace:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or load_settings()
        self.settings.ensure_dirs()
        if self.settings.vector_backend != "memory":
            process_lock.acquire(self.settings.chroma_path)
        self.storage = Storage(self.settings.db_path)
        self.store, self.vector_fallback = create_vector_store(self.settings.vector_backend, self.settings.chroma_path)
        self._lock = threading.RLock()
        self._retrievers: dict[tuple[str, str], Retriever] = {}
        self.progress: dict[str, Any] = {"active": False}

    # ------------------------------------------------------------- plumbing
    def embedder_for(self, backend: str | None = None, model: str | None = None) -> Embedder:
        # A run pinned to hashing stays on hashing; otherwise honour the global setting (auto allows fallback).
        backend = "hashing" if backend == "hashing" else self.settings.embedding_backend
        if backend == "hashing":
            return get_embedder("hashing", "hashing")
        return get_embedder(backend, model if model and not model.startswith("hashing") else self.settings.embedding_model)

    def _retriever(self, embedder: Embedder) -> Retriever:
        key = (embedder.backend, embedder.name)
        if key not in self._retrievers:
            self._retrievers[key] = Retriever(self.storage, self.store, embedder)
        return self._retrievers[key]

    def default_config(self, **overrides: Any) -> RunConfig:
        llm_model = self.settings.llm_model if self.settings.llm_enabled else "offline-extractive"
        config = RunConfig(
            chunk_size=self.settings.chunk_size, chunk_overlap=self.settings.chunk_overlap, top_k=self.settings.top_k,
            embedding_model=self.settings.embedding_model, embedding_backend=self.settings.embedding_backend,
            llm_provider=self.settings.llm_provider, llm_model=llm_model,
        )
        data = config.to_dict()
        data.update({k: v for k, v in overrides.items() if k in data and v is not None})
        return RunConfig.from_dict(data)

    def resolve(self, config: RunConfig) -> tuple[RunConfig, Embedder]:
        """Pin the config to the embedder and generator that will actually run."""
        requested_backend = config.embedding_backend
        embedder = self.embedder_for(requested_backend, config.embedding_model)
        data = config.to_dict()
        data["embedding_backend"] = embedder.backend
        if embedder.backend == "hashing":
            data["embedding_model"] = embedder.name
        if data["chunk_overlap"] >= data["chunk_size"]:
            data["chunk_overlap"] = data["chunk_size"] // 6
        data["llm_provider"] = self.settings.llm_provider
        data["llm_model"] = self.settings.llm_model if self.settings.llm_enabled else "offline-extractive"
        return RunConfig.from_dict(data), embedder

    def status(self) -> dict[str, Any]:
        embedder = self.embedder_for()
        _, fallback = create_generator(self.settings, None) if self.settings.llm_enabled else (None, None)
        return {
            "embedding": {"backend": embedder.backend, "model": embedder.name, "fallback_reason": embedder.fallback_reason},
            "vector_store": {"backend": self.store.backend, "fallback_reason": self.vector_fallback},
            "llm": {"provider": self.settings.llm_provider,
                    "model": self.settings.llm_model if self.settings.llm_enabled else "offline-extractive",
                    "fallback_reason": fallback},
            "ragas": ragas_adapter.status(self.settings.ragas_enabled),
            "limits": {"max_upload_mb": self.settings.max_upload_mb, "max_questions": self.settings.max_questions},
        }

    # ------------------------------------------------------------ documents
    def ingest(self, filename: str, data: bytes) -> tuple[Document, bool]:
        """Parse, store and index a document. Returns (document, created). Duplicates are reused."""
        loaded = load_document(filename, data, self.settings.max_upload_mb)
        with self._lock:
            existing = self.storage.find_document_by_hash(loaded.content_hash)
            if existing:
                return existing, False
            document = Document(
                document_id=new_id("doc"), filename=loaded.filename, file_type=loaded.file_type,
                content_hash=loaded.content_hash, text=loaded.text, metadata=loaded.metadata,
            )
            suffix = Path(loaded.filename).suffix.lower()
            (self.settings.upload_dir / f"{document.document_id}{suffix}").write_bytes(data)
            self.storage.save_document(document)
            config, embedder = self.resolve(self.default_config())
            chunks = self._retriever(embedder).ensure_index(document, config)
            document.metadata["chunk_count"] = len(chunks)
            document.metadata["index_key"] = config.index_key
            self.storage.save_document(document)
            return document, True

    def get_document(self, document_id: str) -> Document:
        document = self.storage.get_document(document_id)
        if document is None:
            raise NotFound(f"Document {document_id} was not found.")
        return document

    def delete_document(self, document_id: str) -> None:
        document = self.get_document(document_id)
        with self._lock:
            self.storage.delete_document(document_id)
            self.store.delete_prefix(f"sq-{document_id}-")
            for path in self.settings.upload_dir.glob(f"{document_id}.*"):
                path.unlink(missing_ok=True)
        log.info("Deleted document %s (%s)", document_id, document.filename)

