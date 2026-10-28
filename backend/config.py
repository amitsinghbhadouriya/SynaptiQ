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
    eval_sets_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "evaluation_sets")
    max_upload_mb: int = 20
    max_questions: int = 50

    # Ragas non-LLM metrics run when the package is installed; set false to skip them
    ragas_enabled: bool = True

    def with_overrides(self, **changes) -> "Settings":
        return replace(self, **changes)

    @property
    def llm_enabled(self) -> bool:
        return self.llm_provider == "anthropic"

    def ensure_dirs(self) -> None:
        for path in (self.chroma_path, self.db_path.parent, self.upload_dir, self.reports_dir):
            path.mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    provider = _env("LLM_PROVIDER", "offline").lower()
    if provider not in {"offline", "anthropic"}:
        provider = "offline"
    return Settings(
        llm_provider=provider,
        llm_model=_env("LLM_MODEL", "claude-opus-5-5"),
        llm_effort=_env("LLM_EFFORT", "low").lower(),
        llm_timeout_s=_env_float("LLM_TIMEOUT_S", 60.0) or 60.0,
        llm_refusal_fallback=_env_bool("LLM_REFUSAL_FALLBACK", True),
        llm_input_price_per_mtok=_env_float("LLM_INPUT_PRICE_PER_MTOK", None),
        llm_output_price_per_mtok=_env_float("LLM_OUTPUT_PRICE_PER_MTOK", None),
        embedding_backend=_env("EMBEDDING_BACKEND", "auto").lower(),
        embedding_model=_env("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        vector_backend=_env("VECTOR_BACKEND", "auto").lower(),
        chunk_size=_env_int("CHUNK_SIZE", 700, 100, 4000),
        chunk_overlap=_env_int("CHUNK_OVERLAP", 100, 0, 1000),
        top_k=_env_int("TOP_K", 4, 1, 20),
        chroma_path=_resolve(_env("CHROMA_PATH", "./storage/chroma")),
        db_path=_resolve(_env("DB_PATH", "./storage/synaptiq.db")),
        upload_dir=_resolve(_env("UPLOAD_DIR", "./storage/uploads")),
        reports_dir=_resolve(_env("REPORTS_DIR", "./reports")),
        max_upload_mb=_env_int("MAX_UPLOAD_MB", 20, 1, 200),
        max_questions=_env_int("MAX_QUESTIONS", 50, 1, 500),
        ragas_enabled=_env_bool("RAGAS_ENABLED", True),
    )

def get_security_config() -> dict:
    """Retrieve security configuration settings with safe defaults."""
    return {
        "rate_limit_per_minute": int(os.environ.get("SYNAPTIQ_RATE_LIMIT", "30")),
        "token_expiry_seconds": int(os.environ.get("SYNAPTIQ_TOKEN_EXPIRY", "3600")),
    }


get_settings = load_settings
