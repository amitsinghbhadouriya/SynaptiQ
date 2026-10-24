# Database & Storage Architecture

This document explains how **SynaptiQ** stores documents, text chunks, test questions, evaluation runs, and mathematical vector embeddings.

---

## 1. Dual-Storage Strategy

SynaptiQ separates its data into two specialized databases:

```
+--------------------------------------------------------------------------+
|                             DATA DIRECTORY                               |
|                         (./storage/ by default)                          |
+------------------------------------+-------------------------------------+
                                     |
         +---------------------------+---------------------------+
         |                                                       |
         v                                                       v
+---------------------------------+     +---------------------------------+
|      SQLITE RELATIONAL DB       |     |        CHROMADB VECTOR DB       |
|    `storage/synaptiq.db`        |     |        `storage/chroma/`        |
|                                 |     |                                 |
| - Original document text        |     | - 384-dimensional dense vectors |
| - Chunk character offsets       |     | - Cosine similarity indices     |
| - QA test questions & evidence  |     | - Fast top-k nearest neighbor   |
| - Baseline vs candidate runs    |     |   search for retriever queries  |
| - Scores, metrics & diagnoses   |     |                                 |
+---------------------------------+     +---------------------------------+
```

### Why two databases?
1. **Relational Data (SQLite)**: Questions, chunk offsets, test runs, and before-and-after comparisons are highly structured. SQLite guarantees that if you delete a document, all of its chunks, questions, and test results are cleaned up safely using `ON DELETE CASCADE`.
2. **Vector Data (ChromaDB)**: Text chunks need to be compared mathematically using cosine similarity. ChromaDB specializes in fast nearest-neighbor search across hundreds of high-dimensional vectors.

---

## 2. SQLite Database Schema (`backend/storage.py`)

SQLite stores all structured data using 5 primary tables:

### Table 1: `documents`
Stores every uploaded document file.
```sql
CREATE TABLE documents (
    document_id   TEXT PRIMARY KEY,       -- e.g. "doc_a1b2c3d4e5"
    filename      TEXT NOT NULL,          -- e.g. "handbook.pdf"
    content_hash  TEXT NOT NULL,          -- SHA-256 hash of file content
    file_type     TEXT NOT NULL,          -- "pdf", "docx", or "txt"
    created_at    TEXT NOT NULL,          -- ISO 8601 UTC timestamp
    status        TEXT NOT NULL,          -- "processed" or "error"
    text          TEXT NOT NULL,          -- Full extracted plain text
    metadata_json TEXT NOT NULL DEFAULT '{}' -- Page bounds & section offsets
);
```

### Table 2: `chunks`
Stores text chunks extracted from documents.
```sql
CREATE TABLE chunks (
    chunk_id      TEXT PRIMARY KEY,       -- e.g. "chk_9f8e7d6c5b"
    document_id   TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    index_key     TEXT NOT NULL,          -- Hash of chunk settings
    chunk_index   INTEGER NOT NULL,       -- 0, 1, 2...
    text          TEXT NOT NULL,          -- Chunk text content
    start_char    INTEGER NOT NULL,       -- Start index in document.text
    end_char      INTEGER NOT NULL,       -- End index in document.text
    page_number   INTEGER,                -- Page number where chunk starts
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX idx_chunks_doc_key ON chunks(document_id, index_key);
```

### Table 3: `evaluation_questions`
Stores benchmark questions with verbatim evidence spans.
```sql
CREATE TABLE evaluation_questions (
    question_id          TEXT PRIMARY KEY,
    document_id          TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    question             TEXT NOT NULL,
    reference_answer     TEXT NOT NULL,
    supporting_chunk_ids TEXT NOT NULL DEFAULT '[]', -- JSON array of chunk IDs
    evidence_json        TEXT NOT NULL DEFAULT '[]', -- Exact char start/end spans
    question_type        TEXT NOT NULL,              -- factual, numerical, multi_hop, unanswerable
    review_status        TEXT NOT NULL,              -- pending, approved, rejected
    source               TEXT NOT NULL,              -- synthetic-offline or claude
    created_at           TEXT NOT NULL
);
```

### Table 4: `evaluation_runs`
Stores the configuration and high-level summary of a test execution.
```sql
CREATE TABLE evaluation_runs (
    run_id             TEXT PRIMARY KEY,  -- e.g. "run_1234567890"
    document_id        TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    dataset_id         TEXT NOT NULL,     -- e.g. "ds_doc_a1b2c3d4e5"
    created_at         TEXT NOT NULL,
    configuration_json TEXT NOT NULL,     -- Full RunConfig parameters
    modes_json         TEXT NOT NULL,     -- ["retriever", "generator", "end_to_end"]
    status             TEXT NOT NULL,     -- queued, running, completed, failed
    duration_ms        INTEGER,
    summary_json       TEXT NOT NULL DEFAULT '{}', -- Pass rate, mean latency
    label              TEXT NOT NULL DEFAULT '',   -- "Baseline" or "Candidate: top-k=2"
