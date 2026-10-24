"""Document ingestion: PDF (PyMuPDF), DOCX (python-docx) and TXT (standard library).

Each loader returns the cleaned full text plus section spans that remember where each
piece came from (page number for PDFs, heading for DOCX/TXT). Errors are raised as
DocumentLoadError with a stable code and a message that is safe to show users.
"""

from __future__ import annotations

import hashlib
import io
import re
import zipfile
from pathlib import Path

from .schemas import LoadedDocument, SectionSpan
from .text_utils import normalize_whitespace

SUPPORTED_TYPES = {".pdf": "PDF", ".docx": "DOCX", ".txt": "TXT"}


class DocumentLoadError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _safe_name(filename: str) -> str:
    name = Path(filename or "document").name
    name = re.sub(r"[^\w.\- ]+", "_", name).strip() or "document"
    return name[:120]


def _assemble(parts: list[tuple[str, int | None, str | None]]) -> tuple[str, list[SectionSpan]]:
    """Join (text, page, label) parts into one text, tracking each part's span."""
    pieces: list[str] = []
    sections: list[SectionSpan] = []
    cursor = 0
    for raw, page, label in parts:
        text = normalize_whitespace(raw)
        if not text:
            continue
        if pieces:
            pieces.append("\n\n")
            cursor += 2
        pieces.append(text)
        sections.append(SectionSpan(start=cursor, end=cursor + len(text), page_number=page, label=label))
        cursor += len(text)
    return "".join(pieces), sections


def _load_pdf(data: bytes) -> tuple[list[tuple[str, int | None, str | None]], dict]:
    if not data.startswith(b"%PDF"):
        raise DocumentLoadError("invalid_content", "The file does not look like a valid PDF.")
    try:
        import pymupdf as fitz  # PyMuPDF >= 1.24 module name
    except ImportError:  # pragma: no cover - older PyMuPDF releases
        try:
