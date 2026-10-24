# REST API Reference

SynaptiQ includes a complete **FastAPI REST API**. When running with `uvicorn backend.api:app --reload`, interactive documentation is available at **`http://localhost:8000/docs`**.

---

## 1. General API Conventions

- **Base URL**: `http://localhost:8000/api/v1`
- **Content-Type**: `application/json` (except document upload which uses `multipart/form-data`)
- **Tracing Header**: Every response includes an `x-request-id` header (e.g. `x-request-id: 7a8b9c0d1e2f`) to correlate server logs.
- **Error Format**: All errors return a JSON object with a `detail` message:
  ```json
  {
    "detail": "Document doc_a1b2c3d4e5 not found"
  }
  ```

---

## 2. System Endpoints

### `GET /api/v1/health`
Checks whether the server and active backends are healthy.

**Response Example (`200 OK`)**:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "environment": {
    "embedding_backend": "sentence-transformers",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "llm_provider": "offline",
    "llm_model": "offline-extractive",
    "device": "cpu",
    "database": "sqlite",
    "vector_store": "chromadb",
    "ragas_available": true
  }
}
```

### `POST /api/v1/demo`
Loads the bundled sample workspace (*Lumen Labs Employee Handbook*) and runs a baseline evaluation with candidate comparison.

**Response Example (`201 Created`)**:
```json
{
  "document_id": "doc_lumen_handbook",
  "baseline_run_id": "run_demo_baseline",
  "candidate_run_id": "run_demo_candidate",
  "pass_rate_baseline": 0.71,
  "pass_rate_candidate": 0.86
}
```

---

## 3. Documents Endpoints

### `POST /api/v1/documents`
Uploads a document (PDF, DOCX, or TXT) for ingestion and chunking.

- **Request**: Multipart form data with a `file` field.
- **Size Limit**: 50 MB by default (`MAX_UPLOAD_MB`).

**Response Example (`201 Created`)**:
```json
{
  "document_id": "doc_e4f5a6b7c8",
  "filename": "security_policy.pdf",
  "status": "processed",
  "chunk_count": 42,
  "created": true
}
```

### `GET /api/v1/documents`
Lists all processed documents stored in the database.

**Response Example (`200 OK`)**:
```json
[
  {
    "document_id": "doc_e4f5a6b7c8",
    "filename": "security_policy.pdf",
    "file_type": "pdf",
    "char_count": 28400,
    "chunk_count": 42,
    "status": "processed",
    "created_at": "2026-10-25T02:00:00Z"
  }
]
```

### `DELETE /api/v1/documents/{document_id}`
Deletes a document along with all associated chunks, vector embeddings, questions, and test runs.

- **Response**: `204 No Content`

---

## 4. Test Sets & Questions Endpoints

### `POST /api/v1/evaluation/questions/generate`
Generates synthetic candidate test questions with verbatim evidence spans.

**Request Body**:
```json
{
  "document_id": "doc_e4f5a6b7c8",
  "count": 10,
  "question_types": ["factual", "numerical", "multi_hop", "unanswerable"]
}
```

**Response Example (`200 OK`)**:
```json
{
  "dataset_id": "ds_doc_e4f5a6b7c8",
  "status": "review_required",
  "candidate_count": 10
}
```

### `GET /api/v1/evaluation/datasets/{dataset_id}`
Retrieves all questions for a given dataset.

**Response Example (`200 OK`)**:
```json
{
  "dataset_id": "ds_doc_e4f5a6b7c8",
  "document_id": "doc_e4f5a6b7c8",
  "questions": [
    {
      "question_id": "q_001",
      "question": "What is the standard password rotation window?",
      "reference_answer": "90 calendar days.",
      "question_type": "factual",
      "review_status": "approved",
      "evidence": [
        {
          "start": 1420,
          "end": 1495,
          "text": "All employee passwords must be rotated every 90 calendar days."
        }
      ]
    }
  ]
}
```

### `PATCH /api/v1/evaluation/questions/{question_id}`
Approve, reject, or edit a generated question.

**Request Body**:
```json
{
  "review_status": "approved",
  "question": "Updated question text",
  "reference_answer": "Updated reference answer"
}
```

---

## 5. Evaluation Runs Endpoints

### `POST /api/v1/evaluation/runs`
Queues or runs an evaluation across the 3 independent modes.

**Query Parameter**:
- `wait=true`: Runs synchronously and returns completed results.
- `wait=false` (default): Queues the job and returns immediately with a poll URL.

**Request Body**:
```json
{
  "dataset_id": "ds_doc_e4f5a6b7c8",
  "modes": ["retriever", "generator", "end_to_end"],
  "configuration": {
    "top_k": 4,
    "chunk_size": 700,
    "chunk_overlap": 100,
    "label": "My Custom Run"
  }
}
```

**Response Example (`202 Accepted`)**:
```json
{
  "run_id": "run_9876543210",
  "status": "queued",
  "poll": "/api/v1/evaluation/runs/run_9876543210"
}
```

### `GET /api/v1/evaluation/runs/{run_id}`
Returns the status, configuration, aggregate metrics, and per-question failure diagnoses of a run.

**Response Example (`200 OK`)**:
```json
{
  "run_id": "run_9876543210",
  "status": "completed",
  "duration_ms": 3420,
  "summary": {
    "pass_rate": 0.85,
    "hit_at_k": 0.90,
    "context_recall": 0.88,
    "faithfulness": 0.92,
    "answer_correctness": 0.84,
    "total_questions": 20,
    "passed_questions": 17
  },
  "results": [
    {
      "question_id": "q_001",
      "diagnosis": "PASS",
      "diagnosis_label": "Pass",
      "diagnosis_reason": "All active modes succeeded."
    }
  ]
}
```

### `POST /api/v1/evaluation/runs/{run_id}/recommendation`
Extracts the top recommended parameter fix from a baseline run and automatically triggers it as a candidate run.

**Response Example (`200 OK`)**:
```json
{
  "run_id": "run_candidate_5521",
  "status": "completed",
  "parent_run_id": "run_9876543210"
}
```

### `POST /api/v1/evaluation/compare`
Compares a baseline run against a candidate run.

**Request Body**:
```json
{
  "baseline_run_id": "run_9876543210",
  "candidate_run_id": "run_candidate_5521",
  "strict": true
}
```

**Response Example (`200 OK`)**:
```json
{
  "baseline_id": "run_9876543210",
  "candidate_id": "run_candidate_5521",
  "pass_rate_change": 0.14,
  "fixed_count": 3,
  "regressed_count": 0,
  "verdict": "Improved performance with zero regressions.",
  "fixed_questions": ["q_004", "q_007", "q_012"],
  "regressed_questions": []
}
```

### `GET /api/v1/evaluation/runs/{run_id}/export?format=csv`
Exports full run data as a downloadable `.csv` or `.json` report.
