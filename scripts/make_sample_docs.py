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
    document = docx.Document()
    for index, (title, paragraphs) in enumerate(parts):
        document.add_heading(title, level=0 if index == 0 else 1)
        for paragraph in paragraphs:
            document.add_paragraph(" ".join(paragraph.split()))
    document.save(out)


def write_pdf(parts, out: Path) -> None:
    pdf = fitz.open()
    page, y = None, 0
    for title, paragraphs in parts:
        blocks = [(title, 15, "hebo")] + [(" ".join(p.split()), 10.5, "helv") for p in paragraphs]
        for text, size, font in blocks:
            if page is None or y > 740:
                page, y = pdf.new_page(), 60
            rect = fitz.Rect(56, y, 540, 800)
            height = page.insert_textbox(rect, text, fontsize=size, fontname=font)
            used = (800 - y) - height if height >= 0 else 0
            y += max(used, size * 1.6) + 10
    pdf.save(out)
    pdf.close()


if __name__ == "__main__":
    parts = list(sections(SOURCE.read_text(encoding="utf-8")))
    write_docx(parts, SOURCE.with_suffix(".docx"))
    write_pdf(parts, SOURCE.with_suffix(".pdf"))
    print("Wrote", SOURCE.with_suffix(".docx").name, "and", SOURCE.with_suffix(".pdf").name)
