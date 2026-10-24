# Testing & Quality Assurance (QA) Guide

This document details the automated testing strategy, test suite structure, and quality assurance workflows for **SynaptiQ**.

---

## 1. Testing Philosophy

The test suite in SynaptiQ adheres to strict quality principles:
- **100% Offline Execution**: The entire test suite runs without downloading external models or requiring internet access.
- **Fast & Lightweight**: All 61+ automated tests complete in under 60 seconds on standard developer laptops.
- **Mocked External APIs**: Cloud services (such as Anthropic Claude) use structured mock responses to ensure deterministic testing without incurring API costs.
- **Zero Flakiness**: Embeddings use deterministic hashing backends during unit tests to guarantee identical vectors across test runs.

---

## 2. Test Suite Architecture (`tests/`)

The automated tests are written using **`pytest`** and organized by functional layer:

| Test File | What It Validates |
|---|---|
| **`test_document_loader.py`** | Tests parsing of PDF, DOCX, and TXT files. Verifies that character offsets accurately map back to source text. Tests error handling for empty files, damaged binaries, and unsupported extensions. |
| **`test_chunking.py`** | Verifies sentence-aware chunk boundaries. Confirms that sentences are never split in half, that overlap is maintained, and that chunk IDs are stable. |
| **`test_retriever.py`** | Validates nearest-neighbor search, top-$k$ chunk filtering, cosine similarity ranking, and evidence coverage calculations. |
| **`test_generator.py`** | Validates offline extractive answer generation, prompt construction, context truncation, and abstention on low-confidence questions. Tests the Claude adapter using a mock Anthropic client. |
| **`test_metrics.py`** | Evaluates all mathematical metrics: Hit@k, Context Recall, Context Precision, MRR, Faithfulness, Answer Correctness, and Abstention. |
| **`test_root_cause.py`** | Exhaustively tests the diagnostic decision tree to verify that all 7 Explainable Outcomes are triggered under the correct conditions. |
| **`test_experiments.py`** | Verifies before-and-after comparison logic, fixed question counts, regression detection, delta calculations, and small-sample warnings. |
| **`test_storage.py`** | Tests SQLite tables, migrations, data integrity, cascade deletion (`ON DELETE CASCADE`), and concurrent access. |
| **`test_api.py`** | End-to-end HTTP tests against all FastAPI REST endpoints (`/api/v1/*`), verifying status codes, schema validation, and error responses. |

---

## 3. How to Run the Tests

Ensure your virtual environment is active, then run:
