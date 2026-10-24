"""Shared data structures. Stable IDs link questions, chunks and results."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

MODES = ("retriever", "generator", "end_to_end")
QUESTION_TYPES = ("factual", "numerical", "multi_hop", "unanswerable")
REVIEW_STATUSES = ("pending", "approved", "rejected")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


@dataclass
class SectionSpan:
    """A slice of the document's full text with its source location."""

    start: int
    end: int
    page_number: int | None = None
    label: str | None = None


@dataclass
class LoadedDocument:
    filename: str
    file_type: str
    content_hash: str
    text: str
    sections: list[SectionSpan]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    document_id: str
    filename: str
    file_type: str
    content_hash: str
    text: str
    status: str = "processed"
    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def sections(self) -> list[SectionSpan]:
        return [SectionSpan(**s) for s in self.metadata.get("sections", [])]

    def page_at(self, offset: int) -> int | None:
        for section in self.sections:
            if section.start <= offset < section.end:
                return section.page_number
        return None

    def summary(self) -> dict[str, Any]:
        data = asdict(self)
        data.pop("text", None)
        data["metadata"] = {k: v for k, v in self.metadata.items() if k != "sections"}
        data["char_count"] = len(self.text)
        return data


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    start_char: int
    end_char: int
    index_key: str
    page_number: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceSpan:
    start: int
    end: int
    text: str


@dataclass
class EvalQuestion:
    question_id: str
    document_id: str
    question: str
    reference_answer: str
    question_type: str = "factual"
    evidence: list[EvidenceSpan] = field(default_factory=list)
    supporting_chunk_ids: list[str] = field(default_factory=list)
    review_status: str = "pending"
    source: str = "synthetic-offline"
    created_at: str = field(default_factory=utc_now)

    @property
    def answerable(self) -> bool:
        return self.question_type != "unanswerable"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvalQuestion":
        payload = dict(data)
        payload["evidence"] = [EvidenceSpan(**e) for e in payload.get("evidence", [])]
        return cls(**{k: v for k, v in payload.items() if k in cls.__dataclass_fields__})


@dataclass
class RunConfig:
    """Everything needed to reproduce a run. Stored with every run."""

    chunk_size: int = 700
    chunk_overlap: int = 100
    top_k: int = 4
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_backend: str = "auto"
    llm_provider: str = "offline"
    llm_model: str = "offline-extractive"
    prompt_version: str = "grounded-v1"
    max_answer_sentences: int = 2
    abstain_threshold: float = 0.3
    label: str = ""

    @property
    def index_key(self) -> str:
        """Chunks and vectors depend only on these settings; reuse the index when they match."""
        raw = f"{self.embedding_backend}|{self.embedding_model}|{self.chunk_size}|{self.chunk_overlap}"
        return hashlib.sha1(raw.encode()).hexdigest()[:10]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
