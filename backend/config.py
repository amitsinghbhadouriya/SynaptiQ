"""Configuration loaded from environment variables (and an optional .env file).

Every setting has a safe local default so the app runs offline out of the box.
Secrets are only read from the environment and are never written to storage.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from pathlib import Path

try:  # python-dotenv is optional at runtime
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if load_dotenv is not None:
    load_dotenv(PROJECT_ROOT / ".env", override=False)


def _env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value and value.strip() else default


def _env_int(name: str, default: int, minimum: int | None = None, maximum: int | None = None) -> int:
    try:
        value = int(_env(name, str(default)))
    except ValueError:
        value = default
    if minimum is not None:
        value = max(minimum, value)
    if maximum is not None:
        value = min(maximum, value)
    return value


def _env_float(name: str, default: float | None) -> float | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _resolve(path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else (PROJECT_ROOT / path).resolve()


@dataclass(frozen=True)
class Settings:
    # LLM provider: "offline" (extractive, no key needed) or "anthropic" (Claude via the official SDK)
    llm_provider: str = "offline"
    llm_model: str = "claude-opus-5-5"
    llm_effort: str = "low"
    llm_timeout_s: float = 60.0
    llm_refusal_fallback: bool = True
    llm_input_price_per_mtok: float | None = None
    llm_output_price_per_mtok: float | None = None

    # Embeddings / vector store
    embedding_backend: str = "auto"  # auto | sentence-transformers | hashing
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_backend: str = "auto"  # auto | chroma | memory

    # Default run configuration
    chunk_size: int = 700
    chunk_overlap: int = 100
    top_k: int = 4

    # Paths and limits
    chroma_path: Path = field(default_factory=lambda: PROJECT_ROOT / "storage" / "chroma")
    db_path: Path = field(default_factory=lambda: PROJECT_ROOT / "storage" / "synaptiq.db")
    upload_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "storage" / "uploads")
    reports_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "reports")
    sample_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "sample_docs")
