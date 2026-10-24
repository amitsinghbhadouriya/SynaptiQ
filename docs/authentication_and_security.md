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

### 1. Reverse Proxy & HTTPS (TLS)
Never expose FastAPI (`port 8000`) or Streamlit (`port 8501`) directly to the public internet. Place them behind a reverse proxy like **Nginx**, **Caddy**, or **Cloudflare** to terminate SSL/TLS encryption.

Example Nginx block:
```nginx
server {
    listen 443 ssl http2;
    server_name synaptiq.internal.company.com;

    ssl_certificate /etc/ssl/synaptiq.crt;
    ssl_certificate_key /etc/ssl/synaptiq.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. API Authentication
When deploying the FastAPI service, add token-based authentication (such as an `X-API-Key` header or OAuth2 Bearer token) using FastAPI dependencies:
```python
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.environ.get("SYNAPTIQ_API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
```

### 3. File Upload Guardrails
- **Max Upload Size**: Controlled via `MAX_UPLOAD_MB=50` in `.env`. Files exceeding this threshold are immediately rejected with HTTP `413 Payload Too Large`.
- **Extension Validation**: Only `.pdf`, `.docx`, and `.txt` MIME types are accepted. Executable files or unknown binaries are rejected with HTTP `422 Unprocessable Entity`.

### 4. Rate Limiting
To prevent denial-of-service (DoS) on vector search or document ingestion, implement rate limiting using libraries such as `slowapi` on the FastAPI endpoints.
