import io

import pytest

from backend.document_loader import DocumentLoadError, load_document


def make_pdf(pages):
    fitz = pytest.importorskip("pymupdf")
    pdf = fitz.open()
    for text in pages:
        page = pdf.new_page()
        if text:
            page.insert_text((72, 72), text, fontsize=11)
    data = pdf.tobytes()
    pdf.close()
    return data


def make_docx():
    docx = pytest.importorskip("docx")
    document = docx.Document()
    document.add_heading("Leave policy", level=1)
    document.add_paragraph("Full-time employees receive 24 days of paid annual leave per calendar year.")
    document.add_heading("Travel", level=1)
    document.add_paragraph("International travel must be approved by a department director.")
    table = document.add_table(rows=2, cols=2)
    table.cell(0, 0).text, table.cell(0, 1).text = "Item", "Limit"
    table.cell(1, 0).text, table.cell(1, 1).text = "Hotel", "150 euros"
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def test_txt_sections_follow_headings(sample_bytes):
    loaded = load_document("handbook.txt", sample_bytes)
    assert loaded.file_type == "TXT"
    labels = [s.label for s in loaded.sections]
    assert "Leave and Time Off" in labels and "Travel and Expenses" in labels
    for section in loaded.sections:  # spans point into the full text
        assert loaded.text[section.start : section.end].strip()


def test_pdf_keeps_page_numbers():
    loaded = load_document("doc.pdf", make_pdf(["First page about leave.", "Second page about travel."]))
