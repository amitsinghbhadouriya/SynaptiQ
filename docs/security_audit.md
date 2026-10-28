# 🛡️ SynaptiQ Security Architecture & Audit Runbook

## Overview
SynaptiQ incorporates defense-in-depth measures to secure the evaluation engine, API gateway, and stored RAG telemetry.

### Core Security Controls
1. **Sliding-Window Rate Limiting**:
   - Default: 30 requests / minute per client token or IP address.
   - Algorithmic implementation: Double-ended timestamp queues (`backend/rate_limiter.py`).
2. **Password Storage**:
   - PBKDF2-HMAC-SHA256 with 100,000 iterations and 16-byte random salt.
3. **Session Revocation**:
   - In-memory JWT ID (`jti`) revocation blacklist (`backend/token_blacklist.py`).
4. **Defensive HTTP Headers**:
   - CSP, HSTS, X-Frame-Options, X-Content-Type-Options (`backend/security_headers.py`).
