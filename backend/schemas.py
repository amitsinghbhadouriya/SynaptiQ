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

