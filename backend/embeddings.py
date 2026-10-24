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
