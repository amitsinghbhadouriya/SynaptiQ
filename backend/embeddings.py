"""Embedding backends.

`SentenceTransformerEmbedder` is the default. When the model cannot be loaded (no
internet on first run, package missing) the app falls back to `HashingEmbedder`, a
deterministic hashed bag-of-words embedding. The active backend and any fallback
reason are recorded with every run so results are never silently mixed.
"""

from __future__ import annotations

import hashlib
import logging
import math
import threading
from typing import Protocol

from .text_utils import content_tokens

log = logging.getLogger(__name__)


class Embedder(Protocol):
    name: str
    backend: str
    dim: int
    fallback_reason: str | None

    def embed(self, texts: list[str]) -> list[list[float]]: ...


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


class HashingEmbedder:
    """Signed feature hashing of unigrams and bigrams with sublinear TF, L2-normalised."""

    backend = "hashing"

    def __init__(self, dim: int = 512, fallback_reason: str | None = None):
        self.dim = dim
        self.name = f"hashing-{dim}"
        self.fallback_reason = fallback_reason

    def _vector(self, text: str) -> list[float]:
        tokens = content_tokens(text)
        features = tokens + [f"{a}_{b}" for a, b in zip(tokens, tokens[1:])]
        counts: dict[int, float] = {}
        for feature in features:
            digest = hashlib.blake2b(feature.encode(), digest_size=8).digest()
            bucket = int.from_bytes(digest[:4], "little") % self.dim
            sign = 1.0 if digest[4] & 1 else -1.0
            weight = 0.5 if "_" in feature else 1.0
            counts[bucket] = counts.get(bucket, 0.0) + sign * weight
        vector = [0.0] * self.dim
        for bucket, value in counts.items():
            vector[bucket] = math.copysign(1 + math.log(abs(value)), value) if value else 0.0
        norm = math.sqrt(sum(v * v for v in vector))
        return [v / norm for v in vector] if norm else vector

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._vector(t) for t in texts]


class SentenceTransformerEmbedder:
    backend = "sentence-transformers"
    fallback_reason = None

    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer  # heavy import, done lazily

        self.name = model_name
        self._model = SentenceTransformer(model_name, device="cpu")
        getter = getattr(self._model, "get_embedding_dimension", None) or self._model.get_sentence_embedding_dimension
        self.dim = int(getter() or 384)
        self._lock = threading.Lock()

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        with self._lock:
            vectors = self._model.encode(
                texts, batch_size=32, normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True
            )
        return [v.tolist() for v in vectors]


_CACHE: dict[tuple[str, str], Embedder] = {}
_CACHE_LOCK = threading.Lock()


def get_embedder(backend: str, model_name: str) -> Embedder:
    """Return a cached embedder; 'auto' tries sentence-transformers and falls back to hashing."""
    backend = (backend or "auto").lower()
    key = (backend, model_name)
    with _CACHE_LOCK:
        if key in _CACHE:
            return _CACHE[key]
        if backend == "hashing":
            embedder: Embedder = HashingEmbedder()
        else:
            try:
                embedder = SentenceTransformerEmbedder(model_name)
            except Exception as exc:  # ImportError, network errors, bad model names
                if backend == "sentence-transformers":
                    raise
                reason = f"{type(exc).__name__}: {str(exc)[:160]}"
                log.warning("Falling back to hashing embeddings (%s)", reason)
                embedder = HashingEmbedder(fallback_reason=reason)
        _CACHE[key] = embedder
        return embedder
