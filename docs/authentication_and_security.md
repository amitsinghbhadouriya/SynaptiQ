# Authentication & Security Guide

This document explains the security architecture, privacy commitments, and best practices for securing **SynaptiQ** in development and production environments.

---

## 1. Core Security & Privacy Philosophy

SynaptiQ was specifically engineered for organizations that handle **proprietary, confidential, or sensitive documents** (such as internal employee manuals, legal contracts, IP documentation, or medical guidelines).

### Three Core Commitments:
1. **100% Offline-First by Default**: 
   When launched out-of-the-box, SynaptiQ makes **zero external network requests**. The text parsing, vector indexing, retrieval, question evaluation, and extractive answer generation all execute locally on your own machine.
2. **Zero External Telemetry**: 
   SynaptiQ contains **no tracking beacons**, no Google Analytics, no phone-home telemetry, and no hidden usage reporting. Your documents and test results never leave your environment.
3. **Local Data Residency**: 
   All uploaded files, text chunks, vector embeddings (ChromaDB), and relational run histories (SQLite) reside strictly in the `./storage/` folder on your local disk.

---

## 2. Managing Sensitive Documents

When evaluating proprietary knowledge bases:
- **Default Offline Mode**: Keep `LLM_PROVIDER=offline` in your `.env` file. This guarantees that your document text is never sent to any third-party cloud API.
- **Third-Party LLM Notice (Claude)**: If you explicitly configure Anthropic Claude (`LLM_PROVIDER=anthropic`), document chunks will be sent to Anthropic's API to generate answers and synthetic questions. **Only enable this for documents you are authorized to share with an external AI provider.**
- **Safe Logging**: The FastAPI and Streamlit loggers are explicitly configured to log metadata (file size, chunk count, request IDs, and latency) **without logging document text or query contents**.

---

## 3. Storage Security & File Permissions

- **SQLite Database**: Stored at `./storage/synaptiq.db`. Ensure that appropriate file-system permissions restrict read/write access to the specific operating system user running the process.
- **ChromaDB Vector Store**: Stored under `./storage/chroma/`. Contains raw text chunks and floating-point embedding arrays.
- **Process Lock**: A lock file (`./storage/synaptiq.lock`) is maintained by `backend/process_lock.py` to prevent race conditions and concurrent write corruption.

---

## 4. Hardening SynaptiQ for Production Deployment

By default, SynaptiQ binds to `localhost` (`127.0.0.1`), intended for private developer use. **If you plan to expose SynaptiQ across a local network or on a public server, apply the following protections:**

