# Feature Development & Extension Guide

This guide explains how developers can extend **SynaptiQ** to add new file formats, custom chunking algorithms, new embedding backends, additional evaluation metrics, or new dashboard tabs.

---

## 1. Project Coding Standards

- **Python Version**: Python 3.11 / 3.12 compatibility.
- **Data Models**: Use `@dataclass` from the standard library for data containers (defined in `backend/schemas.py`).
- **Type Annotations**: Always include full Python type hints (`int`, `str | None`, `list[str]`, etc.).
- **Deterministic & Offline First**: Any new feature should work offline by default or have an offline fallback.
- **Testing Requirement**: Every new backend feature must include automated unit tests under `tests/`.

---

## 2. Adding a New Document Parser

All document loading lives in **`backend/document_loader.py`**.

To add support for a new format (for example, Markdown `.md`):
1. In `backend/document_loader.py`, find the `load_document` function.
2. Add the file extension check:
   ```python
   elif ext == ".md":
       text, sections = _load_markdown(data)
   ```
3. Implement the extractor function:
   ```python
   def _load_markdown(raw_bytes: bytes) -> tuple[str, list[SectionSpan]]:
       text = raw_bytes.decode("utf-8", errors="replace")
       # Extract sections based on "# " or "## " headings
       sections = []
       # ... track character start and end offsets ...
       return text, sections
   ```
4. Add a test in `tests/test_document_loader.py` to verify character offsets and empty-file handling.

---

## 3. Adding a Custom Chunking Strategy

Chunking logic lives in **`backend/chunking.py`**.

To add a new chunking algorithm (e.g., Semantic Chunking or Recursive Token Chunking):
1. Inspect the signature of `chunk_text`:
   ```python
   def chunk_text(
       text: str,
       chunk_size: int,
       chunk_overlap: int,
       document_id: str,
       index_key: str,
       strategy: str = "sentence",
   ) -> list[Chunk]:
   ```
2. Implement your splitting algorithm ensuring that:
   - Every chunk records its exact `start_char` and `end_char` within `text`.
   - Every chunk is assigned a stable ID: `chk_{document_id}_{index}`.
3. Add a unit test in `tests/test_chunking.py` verifying that reconstructed text matches source offsets.

---

## 4. Adding a New Embedding Model or Backend

Embedding generation lives in **`backend/embeddings.py`**.

SynaptiQ defines a clean base interface:
```python
class EmbeddingBackend:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_query(self, query: str) -> list[float]:
        raise NotImplementedError
```

To add a new provider (e.g., local Ollama or OpenAI embeddings):
1. Create a new subclass:
   ```python
   class OllamaEmbeddingBackend(EmbeddingBackend):
       def __init__(self, model_name: str = "nomic-embed-text"):
           self.model_name = model_name

       def embed_texts(self, texts: list[str]) -> list[list[float]]:
           # Call local ollama HTTP API
           ...

       def embed_query(self, query: str) -> list[float]:
           return self.embed_texts([query])[0]
   ```
2. Register the backend in `create_embedding_backend()` in `backend/embeddings.py`.

---

## 5. Adding a Custom Evaluation Metric
