"""Create PDF and DOCX copies of the sample handbook for trying out uploads.

    python scripts/make_sample_docs.py

Uses PyMuPDF and python-docx (both in requirements.txt). The TXT file stays the source.
"""

from pathlib import Path

import docx
import pymupdf as fitz

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "sample_docs" / "lumen_labs_handbook.txt"


def sections(text: str):
    title, body = None, []
    for line in text.splitlines():
        if line.startswith("# "):
            if title or body:
                yield title, [p for p in "\n".join(body).split("\n\n") if p.strip()]
            title, body = line[2:].strip(), []
        else:
            body.append(line)
    yield title, [p for p in "\n".join(body).split("\n\n") if p.strip()]


def write_docx(parts, out: Path) -> None:
