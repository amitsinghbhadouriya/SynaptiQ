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
    assert loaded.file_type == "PDF"
    assert [s.page_number for s in loaded.sections] == [1, 2]
    assert "Second page about travel." in loaded.text
    assert loaded.metadata["pages"] == 2


def test_docx_headings_and_tables():
    loaded = load_document("policy.docx", make_docx())
    labels = [s.label for s in loaded.sections]
    assert "Leave policy" in labels and "Travel" in labels and "Table 1" in labels
    assert "Hotel | 150 euros" in loaded.text


@pytest.mark.parametrize(
    "name,data,code",
    [
        ("notes.md", b"hello", "unsupported_type"),
        ("empty.txt", b"", "empty_file"),
        ("fake.pdf", b"not a pdf at all", "invalid_content"),
        ("fake.docx", b"plain text", "invalid_content"),
        ("binary.txt", b"\x00\x01\x02binary", "invalid_content"),
    ],
)
def test_invalid_files_raise_safe_errors(name, data, code):
    with pytest.raises(DocumentLoadError) as excinfo:
        load_document(name, data)
    assert excinfo.value.code == code


def test_size_limit():
    with pytest.raises(DocumentLoadError) as excinfo:
        load_document("big.txt", b"a" * (1024 * 1024 + 10), max_upload_mb=1)
    assert excinfo.value.code == "too_large"


def test_pdf_without_text_mentions_ocr():
    with pytest.raises(DocumentLoadError) as excinfo:
        load_document("scan.pdf", make_pdf([""]))
    assert excinfo.value.code == "no_text"
    assert "OCR" in excinfo.value.message


def test_filename_is_sanitised(sample_bytes):
    loaded = load_document("../../etc/evil<name>.txt", sample_bytes)
    assert "/" not in loaded.filename and "<" not in loaded.filename
