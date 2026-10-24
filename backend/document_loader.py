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
            import fitz
        except ImportError as exc:
            raise DocumentLoadError("missing_dependency", "PyMuPDF is required to read PDF files.") from exc
    try:
        with fitz.open(stream=data, filetype="pdf") as pdf:
            if pdf.needs_pass:
                raise DocumentLoadError("encrypted", "Password-protected PDFs are not supported.")
            parts = [(page.get_text("text"), index + 1, f"Page {index + 1}") for index, page in enumerate(pdf)]
            meta = {"pages": pdf.page_count, "title": (pdf.metadata or {}).get("title") or None}
    except DocumentLoadError:
        raise
    except Exception as exc:
        raise DocumentLoadError("parse_failed", "The PDF could not be parsed; it may be damaged.") from exc
    return parts, meta


def _load_docx(data: bytes) -> tuple[list[tuple[str, int | None, str | None]], dict]:
    if not data.startswith(b"PK") or not zipfile.is_zipfile(io.BytesIO(data)):
        raise DocumentLoadError("invalid_content", "The file does not look like a valid DOCX document.")
    try:
        import docx  # python-docx
    except ImportError as exc:  # pragma: no cover
        raise DocumentLoadError("missing_dependency", "python-docx is required to read DOCX files.") from exc
    try:
        document = docx.Document(io.BytesIO(data))
    except Exception as exc:
        raise DocumentLoadError("parse_failed", "The DOCX file could not be parsed; it may be damaged.") from exc

    parts: list[tuple[str, int | None, str | None]] = []
    heading = "Introduction"
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            parts.append(("\n".join(buffer), None, heading))
            buffer.clear()

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue
        style = (paragraph.style.name if paragraph.style is not None else "") or ""
        if style.lower().startswith(("heading", "title")):
            flush()
            heading = text[:80]
            buffer.append(text)
        else:
            buffer.append(text)
    flush()
    for index, table in enumerate(document.tables):
        rows = [" | ".join(cell.text.strip() for cell in row.cells) for row in table.rows]
        parts.append(("\n".join(r for r in rows if r.strip(" |")), None, f"Table {index + 1}"))
    return parts, {"paragraphs": len(document.paragraphs), "tables": len(document.tables)}


def _load_txt(data: bytes) -> tuple[list[tuple[str, int | None, str | None]], dict]:
    if b"\x00" in data[:4096]:
        raise DocumentLoadError("invalid_content", "The file looks binary, not plain text.")
    for encoding in ("utf-8-sig", "utf-16") if data[:2] in (b"\xff\xfe", b"\xfe\xff") else ("utf-8-sig", "cp1252", "latin-1"):
