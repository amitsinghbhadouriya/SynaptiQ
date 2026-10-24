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
