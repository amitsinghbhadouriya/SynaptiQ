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
  - `chunk_overlap` (e.g. 100 characters)
- **Sentence Integrity**: Never cuts a sentence in half. If a chunk boundary lands mid-sentence, it searches backwards for the last period, exclamation mark, or newline to keep thoughts intact.
- **Stable IDs**: Assigns a unique, deterministic ID (`chk_<document_id>_<index>`) to every chunk.

---

### Stage 4: Embedding Generation (`backend/embeddings.py`)
- Converts each text chunk into a 384-dimensional mathematical vector.
- **Default Engine**: **Sentence Transformers** using the `all-MiniLM-L6-v2` model (~90 MB, runs fast on CPU).
- **Offline Hashing Fallback**: If internet access is unavailable to download the model, SynaptiQ automatically falls back to deterministic lexical hashing vectors (`HashingEmbeddingBackend`). No runs will ever crash due to missing internet.

---

### Stage 5: Vector Store Indexing (`backend/vector_store.py`)
- Saves the vector embeddings into local **ChromaDB** collections.
- **Index Caching**: Calculates an `index_key` hash:
  $$\text{index\_key} = \text{SHA1}(\text{backend} + \text{model} + \text{chunk\_size} + \text{chunk\_overlap})[:10]$$
  If another run is started with the same chunking and model settings, SynaptiQ instantly reuses the indexed collection rather than recomputing embeddings.

---

### Stage 6: Test Set Preparation (`backend/synthetic_qa.py`)
- Loads benchmark questions, reference answers, and **verbatim evidence quotes**.
- **Quote Verification**: The loader locates the exact character start and end span of every evidence quote in the source document. If a quote cannot be found, it is rejected to ensure benchmarks are 100% grounded.

---

### Stage 7: Retriever Search (`backend/retriever.py`)
- For each test question, converts the query text into a vector and searches ChromaDB using cosine distance.
- Returns the top-$k$ most similar chunks (e.g. $k=1, 2, 4,$ etc.), ranked from most similar to least similar.
- Calculates whether each retrieved chunk contains the reference evidence spans.

---

### Stage 8: Generator Response (`backend/generator.py`)
- Produces answers under two different modes:
  1. **Offline Extractive Mode (Default)**: Uses transparent sentence-matching heuristics to extract the most relevant factual answer directly from the supplied context. Completely offline and instant.
