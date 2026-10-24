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
  2. **Claude API Mode (Optional)**: Calls Anthropic Claude (`claude-opus-5-5` or configured model) with a grounded prompt that instructs the model to rely only on the retrieved context.
- **Abstention Logic**: If the maximum similarity score between the question and context is below the `abstain_threshold`, the generator gracefully declines to answer to avoid hallucinations.

---

### Stage 9: Multi-Metric Scoring (`backend/metrics.py` & `ragas_adapter.py`)
Scores the output across multiple transparent metrics:
- **Hit@k**: `1.0` if all evidence spans are at least 50% covered by the top-$k$ chunks.
- **Context Recall**: The percentage of reference evidence characters present in the retrieved chunks.
- **Context Precision**: Rank-aware score evaluating whether evidence chunks appear near the top of the search results.
- **First Relevant Rank (MRR)**: The exact position (#1, #2, #3...) where the first supporting chunk appeared.
- **Answer Correctness**: Blends token recall (0.65) and semantic similarity (0.35). Capped at 0.4 if a required reference number is missing.
- **Faithfulness**: Share of answer sentences directly backed by the retrieved context.
- **Abstention Correctness**: Verifies if unanswerable questions were correctly declined.

---

### Stage 10: Root-Cause Diagnosis (`backend/root_cause.py`)
- Evaluates the three independent test results (`retriever`, `generator`, `end_to_end`).
- Uses deterministic diagnostic rules to assign one of the **7 Explainable Outcomes** (e.g. *Retrieval Failure*, *Generation Failure*, *Pipeline Interaction*, or *Pass*).

---

### Stage 11: Targeted Recommendations (`backend/recommendations.py`)
- Translates failure evidence into a single, concrete setting adjustment:
  - Suggests higher `top_k` if evidence was ranked just outside the window.
  - Suggests larger `chunk_size` or `chunk_overlap` if evidence was cut across chunk seams.
  - Suggests a stronger embedding model if evidence never appeared in search.
  - Suggests strict prompts or higher abstention thresholds if hallucinating.

---

### Stage 12: Experiment Comparison & Reports (`backend/experiments.py` & `reports.py`)
- Executes the candidate configuration on the exact same question set.
- Calculates the before-and-after delta (e.g., pass rate changed from 71% to 86%).
- Identifies newly fixed questions and flags any regressions.
- Generates downloadable CSV/JSON exports and interactive Plotly visualization charts.
