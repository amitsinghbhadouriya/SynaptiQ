# Project Implementation Guide

This document walks you step-by-step through the **12-stage engineering pipeline** inside **SynaptiQ**, explaining exactly how text transforms from a raw uploaded document into an evidence-backed optimization report.

---

## The 12-Stage Pipeline

```
 [1. Ingest]  -->  [2. Normalize]  -->  [3. Chunk]  -->  [4. Embed]
      |
      v
 [5. Index]   -->  [6. Test Set]   -->  [7. Retrieve] --> [8. Generate]
      |
      v
 [9. Score]   -->  [10. Diagnose]  -->  [11. Recommend] -> [12. Verify & Report]
```

---

### Stage 1: Document Ingestion (`backend/document_loader.py`)
- **Supported Formats**: PDF, DOCX, and TXT files.
- **Engines**: Uses **PyMuPDF (`fitz`)** for PDF extraction, **python-docx** for Word documents, and Python standard library for UTF-8 text.
- **Integrity Checks**: Detects empty documents, scanned image-only PDFs (which require OCR), and encrypted or damaged files.
- **Content Hash**: Generates a SHA-256 fingerprint of the file bytes to prevent duplicate ingestion.

---

### Stage 2: Character Normalization & Section Tracking
- Extracts plain text while strictly recording where each page and heading starts and ends using **character offsets** (`start_char` to `end_char`).
- This character map allows any chunk or evidence quote to be traced back to the exact page and paragraph in the original file.

---

### Stage 3: Sentence-Aware Chunking (`backend/chunking.py`)
- Cuts continuous text into smaller passages based on two configuration settings:
  - `chunk_size` (e.g. 700 characters)
