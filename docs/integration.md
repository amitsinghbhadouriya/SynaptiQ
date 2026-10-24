# Integrations Guide

This guide explains how to connect **SynaptiQ** with external Language Models (LLMs), local AI servers, custom RAG pipelines, and automated CI/CD workflows.

---

## 1. Connecting Anthropic Claude

SynaptiQ includes built-in, native support for **Anthropic Claude** via the official Python `anthropic` SDK.

### Setup Instructions
1. Open your `.env` file (copied from `.env.example`).
2. Configure the following keys:
   ```dotenv
   LLM_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-api03-your-actual-api-key-here
   LLM_MODEL=claude-opus-5-5
   LLM_EFFORT=low
   LLM_REFUSAL_FALLBACK=true
   ```

### What Claude Does in SynaptiQ:
- **Grounded Answer Generation**: Uses a strictly instructed prompt that treats document text as untrusted data and forbids using outside knowledge.
- **High-Quality Synthetic Questions**: When generating test sets, Claude creates natural, nuanced questions paired with verbatim quotes found in the text.
- **Token Cost Tracking**: Automatically calculates real-time estimated dollar costs per query based on published per-token pricing.

---

## 2. Connecting Local LLMs (Ollama / vLLM / LM Studio)

If you require advanced generative capabilities but cannot send data to cloud APIs, you can easily connect a local LLM engine such as **Ollama**:

### Example Ollama Adapter in `backend/generator.py`:
```python
import httpx

class OllamaGenerator(Generator):
    def __init__(self, model_name: str = "llama3:8b", endpoint: str = "http://localhost:11434"):
        self.model_name = model_name
        self.endpoint = endpoint

    def generate(self, question: str, contexts: list[str]) -> str:
        prompt = f"Answer the question using ONLY the provided context.\n\nContext:\n{'\n'.join(contexts)}\n\nQuestion: {question}"
        response = httpx.post(
            f"{self.endpoint}/api/generate",
            json={"model": self.model_name, "prompt": prompt, "stream": False},
            timeout=60.0
        )
        return response.json().get("response", "")
```

---

## 3. Alternative Embedding Models (Hugging Face)

By default, SynaptiQ uses `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions), which is extremely fast and light. 

You can switch to any other Sentence Transformer model by setting:
```dotenv
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```
or for multilingual documents:
```dotenv
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```
When changed, SynaptiQ automatically re-indexes the vectors into a dedicated collection without interfering with prior runs.

---

## 4. Integrating with Your Existing RAG Pipeline

If your team already has an existing RAG system (built on **LangChain**, **LlamaIndex**, or custom Python code), you can use SynaptiQ as an **external evaluation and diagnostic harness** via its REST API:

### Workflow:
1. **Import Documents**: Call `POST /api/v1/documents` to ingest your knowledge base.
2. **Import or Generate Test Questions**: Call `POST /api/v1/evaluation/questions/import` with your existing test questions and evidence quotes.
3. **Trigger Evaluation**: Call `POST /api/v1/evaluation/runs?wait=true`.
4. **Inspect Failure Diagnoses**: Fetch results from `GET /api/v1/evaluation/runs/{run_id}` to see if any questions experienced Retrieval Failures or Generation Failures.
5. **Get Concrete Recommendations**: Call `POST /api/v1/evaluation/runs/{run_id}/recommendation` to see what configuration change improves the pass rate.

---

## 5. CI/CD Automated Regression Testing

You can run SynaptiQ inside your **GitHub Actions** or **GitLab CI** pipelines to ensure that changes to your prompts, chunking, or documents do not cause regressions:

```yaml
# Example GitHub Actions step
name: RAG Evaluation Benchmark

on: [push, pull_request]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run SynaptiQ Evaluation Suite
        run: |
          pytest tests/ -v
```
