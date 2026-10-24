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
