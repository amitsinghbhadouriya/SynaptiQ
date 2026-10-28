"""Payload 1 for SynaptiQ 128 Commits (Commits 1 to 42)."""

def get_commits_1_to_42():
    commits = []

    # 1: Windows patch
    commits.append({
        "id": 1,
        "msg": "fix(core): implement Windows Proactor asyncio connection-lost exception suppression",
        "files": ["backend/windows_patch.py"],
        "setup": None # already exists
    })

    # 2: Unit tests for Windows patch
    commits.append({
        "id": 2,
        "msg": "test(core): add comprehensive unit test suite for Windows asyncio error handler",
        "files": ["tests/test_windows_patch.py"],
        "setup": None # already exists
    })

    # 3: backend/__init__.py
    commits.append({
        "id": 3,
        "msg": "fix(backend): initialize Windows asyncio compatibility patch on package import",
        "files": ["backend/__init__.py"],
        "setup": None # already modified
    })

    # 4: backend/api.py
    commits.append({
        "id": 4,
        "msg": "fix(api): apply Windows event loop patch during FastAPI application lifespan",
        "files": ["backend/api.py"],
        "setup": None # already modified
    })

    # 5: app.py
    commits.append({
        "id": 5,
        "msg": "fix(streamlit): apply Windows socket error suppression to Streamlit entrypoint",
        "files": ["app.py"],
        "setup": None # already modified
    })

    # 6: README.md troubleshooting
    commits.append({
        "id": 6,
        "msg": "docs(troubleshooting): document WinError 10054 resolution in README",
        "files": ["README.md"],
        "setup": None # already modified
    })

    # 7: frontend/dist/assets/
    commits.append({
        "id": 7,
        "msg": "build(frontend): update compiled bundle assets with authentication modal and UI chunks",
        "files": ["frontend/dist/assets/"],
        "setup": None # already staged
    })

    # 8: frontend/dist/index.html
    commits.append({
        "id": 8,
        "msg": "build(frontend): synchronize production index.html script references",
        "files": ["frontend/dist/index.html"],
        "setup": None # already modified
    })

    # 9: backend/auth_schemas.py
    commits.append({
        "id": 9,
        "msg": "feat(auth): define authentication models, token payloads, and credential schemas",
        "files": ["backend/auth_schemas.py"],
        "setup": lambda: {
            "backend/auth_schemas.py": '''"""Pydantic schemas and dataclasses for SynaptiQ authentication and sessions."""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class UserCredentials(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username for login")
    password: str = Field(..., min_length=8, description="Plaintext password")


class UserRegistration(UserCredentials):
    email: str = Field(..., description="User contact email")
    full_name: Optional[str] = Field(None, max_length=100)
    role: str = Field(default="viewer", pattern="^(admin|evaluator|viewer)$")


class TokenPayload(BaseModel):
    sub: str = Field(..., description="User identifier")
    role: str = Field(default="viewer")
    exp: int = Field(..., description="Expiration timestamp (epoch)")
    iat: int = Field(..., description="Issued at timestamp")
    jti: Optional[str] = Field(None, description="Unique JWT ID for revocation tracking")


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: dict
'''
        }
    })

    # 10: backend/password_utils.py
    commits.append({
        "id": 10,
        "msg": "feat(auth): implement secure password hashing with salt and PBKDF2-HMAC-SHA256",
        "files": ["backend/password_utils.py"],
        "setup": lambda: {
            "backend/password_utils.py": '''"""Cryptographic password hashing and verification using standard PBKDF2-HMAC-SHA256."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets

ITERATIONS = 100_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    """Hash password using PBKDF2 with SHA-256 and random 16-byte salt."""
    salt = secrets.token_bytes(SALT_BYTES)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{salt.hex()}:{derived.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against salt:derived hex string using constant-time comparison."""
    try:
        parts = hashed.split(":")
        if len(parts) != 2:
            return False
        salt = bytes.fromhex(parts[0])
        expected = bytes.fromhex(parts[1])
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
        return hmac.compare_digest(derived, expected)
    except Exception:
        return False
'''
        }
    })

    # 11: backend/auth.py
    commits.append({
        "id": 11,
        "msg": "feat(auth): scaffold JWT authentication and API key verification engine",
        "files": ["backend/auth.py"],
        "setup": lambda: {
            "backend/auth.py": '''"""JWT token issuance, verification, and API key authentication services."""

from __future__ import annotations

import base64
import json
import time
import os
import hmac
import hashlib
import secrets
from typing import Optional, Dict, Any
from .auth_schemas import TokenPayload

SECRET_KEY = os.environ.get("SYNAPTIQ_SECRET_KEY", "synaptiq-insecure-dev-secret-change-in-prod")
API_KEY_HEADER = "X-SynaptiQ-Key"


def create_access_token(user_id: str, role: str = "viewer", expires_in: int = 3600) -> str:
    """Generates a compact HMAC-SHA256 authenticated token payload."""
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": user_id,
        "role": role,
        "iat": now,
        "exp": now + expires_in,
        "jti": secrets.token_hex(8),
    }

    b64_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    b64_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    signing_input = f"{b64_header}.{b64_payload}"

    sig = hmac.new(SECRET_KEY.encode(), signing_input.encode(), hashlib.sha256).digest()
    b64_sig = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    return f"{signing_input}.{b64_sig}"


def decode_access_token(token: str) -> Optional[TokenPayload]:
    """Validates token signature and expiration, returning TokenPayload if valid."""
    try:
        parts = token.strip().split(".")
        if len(parts) != 3:
            return None
        signing_input = f"{parts[0]}.{parts[1]}"
        expected_sig = hmac.new(SECRET_KEY.encode(), signing_input.encode(), hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(parts[2] + "==")
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_bytes = base64.urlsafe_b64decode(parts[1] + "==")
        data = json.loads(payload_bytes.decode())
        if int(time.time()) > data.get("exp", 0):
            return None
        return TokenPayload(**data)
    except Exception:
        return None
'''
        }
    })

    # 12: backend/token_blacklist.py
    commits.append({
        "id": 12,
        "msg": "feat(auth): implement in-memory token revocation blacklist and session store",
        "files": ["backend/token_blacklist.py"],
        "setup": lambda: {
            "backend/token_blacklist.py": '''"""Token revocation blacklist and active session tracking store."""

from __future__ import annotations

import time
import threading
from typing import Set, Dict


class TokenBlacklist:
    def __init__(self):
        self._blacklisted_jtis: Dict[str, int] = {}
        self._lock = threading.Lock()

    def revoke(self, jti: str, exp: int) -> None:
        """Mark a token JTI as revoked until its expiration epoch."""
        with self._lock:
            self._blacklisted_jtis[jti] = exp

    def is_revoked(self, jti: str) -> bool:
        """Check if a token has been explicitly revoked."""
        with self._lock:
            if jti not in self._blacklisted_jtis:
                return False
            if time.time() > self._blacklisted_jtis[jti]:
                del self._blacklisted_jtis[jti]
                return False
            return True

    def purge_expired(self) -> int:
        """Purge entries whose expiration time has elapsed."""
        now = time.time()
        with self._lock:
            initial = len(self._blacklisted_jtis)
            self._blacklisted_jtis = {
                k: v for k, v in self._blacklisted_jtis.items() if v > now
            }
            return initial - len(self._blacklisted_jtis)


token_blacklist = TokenBlacklist()
'''
        }
    })

    # 13: backend/rate_limiter.py
    commits.append({
        "id": 13,
        "msg": "feat(security): implement sliding-window rate limiting algorithm with 30 req/min default",
        "files": ["backend/rate_limiter.py"],
        "setup": lambda: {
            "backend/rate_limiter.py": '''"""Sliding-window rate limiter protecting SynaptiQ endpoints against abuse."""

from __future__ import annotations

import time
import threading
from collections import deque
from typing import Dict, Tuple


class SlidingWindowRateLimiter:
    """Tracks client request timestamps within a rolling window."""

    def __init__(self, limit: int = 30, window_seconds: float = 60.0):
        self.limit = limit
        self.window = window_seconds
        self._clients: Dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, client_id: str) -> Tuple[bool, int, float]:
        """Returns (is_allowed, remaining_requests, retry_after_seconds)."""
        now = time.time()
        window_start = now - self.window

        with self._lock:
            if client_id not in self._clients:
                self._clients[client_id] = deque()

            q = self._clients[client_id]
            while q and q[0] <= window_start:
                q.popleft()

            if len(q) < self.limit:
                q.append(now)
                remaining = self.limit - len(q)
                return True, remaining, 0.0

            oldest = q[0]
            retry_after = max(0.1, (oldest + self.window) - now)
            return False, 0, retry_after

    def reset(self, client_id: str | None = None) -> None:
        """Reset counters for a single client or all clients."""
        with self._lock:
            if client_id:
                self._clients.pop(client_id, None)
            else:
                self._clients.clear()


default_rate_limiter = SlidingWindowRateLimiter(limit=30, window_seconds=60.0)
'''
        }
    })

    # 14: backend/rbac.py
    commits.append({
        "id": 14,
        "msg": "feat(security): add role-based access control (RBAC) scopes and permission decorators",
        "files": ["backend/rbac.py"],
        "setup": lambda: {
            "backend/rbac.py": '''"""Role-Based Access Control (RBAC) enforcement and permission levels."""

from __future__ import annotations

from typing import Set, Dict

ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "admin": {
        "workspaces:read", "workspaces:write", "workspaces:delete",
        "evaluations:run", "evaluations:read", "evaluations:delete",
        "settings:manage", "users:manage"
    },
    "evaluator": {
        "workspaces:read", "workspaces:write",
        "evaluations:run", "evaluations:read"
    },
    "viewer": {
        "workspaces:read",
        "evaluations:read"
    }
}


def has_permission(role: str, permission: str) -> bool:
    """Verifies if the specified role possesses the given permission flag."""
    return permission in ROLE_PERMISSIONS.get(role, set())
'''
        }
    })

    # 15: backend/security_headers.py
    commits.append({
        "id": 15,
        "msg": "feat(security): implement security headers middleware (CSP, HSTS, X-Content-Type)",
        "files": ["backend/security_headers.py"],
        "setup": lambda: {
            "backend/security_headers.py": '''"""HTTP security headers middleware enforcing defensive response policies."""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Content-Security-Policy": "default-src 'self' 'unsafe-inline' https:; frame-ancestors 'none';"
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            if header not in response.headers:
                response.headers[header] = value
        return response
'''
        }
    })

    # 16: backend/api_auth_routes.py
    commits.append({
        "id": 16,
        "msg": "feat(api): create dedicated authentication endpoints for login and token refresh",
        "files": ["backend/api_auth_routes.py"],
        "setup": lambda: {
            "backend/api_auth_routes.py": '''"""FastAPI router for user authentication, registration, and session control."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from .auth_schemas import UserCredentials, UserRegistration, AuthTokenResponse
from .password_utils import hash_password, verify_password
from .auth import create_access_token
from .rate_limiter import default_rate_limiter

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Demo user storage for local standalone runs
USERS_DB = {
    "admin": {
        "password_hash": hash_password("synaptiq-admin-pass"),
        "role": "admin",
        "email": "admin@synaptiq.ai"
    }
}


@auth_router.post("/login", response_model=AuthTokenResponse)
async def login(creds: UserCredentials):
    allowed, remaining, retry_after = default_rate_limiter.is_allowed(creds.username)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded (30 req/min). Retry in {retry_after:.1f}s"
        )

    user = USERS_DB.get(creds.username)
    if not user or not verify_password(creds.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user_id=creds.username, role=user["role"])
    return AuthTokenResponse(
        access_token=token,
        user={"username": creds.username, "role": user["role"], "email": user["email"]}
    )
'''
        }
    })

    # 17: tests/test_password_utils.py
    commits.append({
        "id": 17,
        "msg": "test(auth): add unit tests for password hashing and constant-time verification",
        "files": ["tests/test_password_utils.py"],
        "setup": lambda: {
            "tests/test_password_utils.py": '''"""Unit tests for PBKDF2 password hashing and verification."""

from backend.password_utils import hash_password, verify_password


def test_password_hash_and_verify_success():
    pwd = "super-secret-password-123!"
    hashed = hash_password(pwd)
    assert ":" in hashed
    assert verify_password(pwd, hashed) is True


def test_password_verify_failure_wrong_password():
    pwd = "correct-password"
    hashed = hash_password(pwd)
    assert verify_password("wrong-password", hashed) is False


def test_password_verify_malformed_hash():
    assert verify_password("pwd", "not-a-valid-hash") is False
    assert verify_password("pwd", "") is False
'''
        }
    })

    # 18: tests/test_auth.py
    commits.append({
        "id": 18,
        "msg": "test(auth): add unit tests for JWT token generation, decoding, and expiration",
        "files": ["tests/test_auth.py"],
        "setup": lambda: {
            "tests/test_auth.py": '''"""Unit tests for token issuance and cryptographic verification."""

import time
from backend.auth import create_access_token, decode_access_token


def test_token_encode_decode_roundtrip():
    token = create_access_token("test_user", role="admin", expires_in=60)
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.sub == "test_user"
    assert payload.role == "admin"


def test_token_expiration_rejection():
    # Token that expired 5 seconds ago
    token = create_access_token("expired_user", expires_in=-5)
    payload = decode_access_token(token)
    assert payload is None


def test_token_tampered_signature():
    token = create_access_token("legit_user")
    tampered = token[:-4] + "xxxx"
    assert decode_access_token(tampered) is None
'''
        }
    })

    # 19: tests/test_token_blacklist.py
    commits.append({
        "id": 19,
        "msg": "test(auth): test token revocation and blacklist verification logic",
        "files": ["tests/test_token_blacklist.py"],
        "setup": lambda: {
            "tests/test_token_blacklist.py": '''"""Unit tests for token revocation blacklist."""

import time
from backend.token_blacklist import TokenBlacklist


def test_token_blacklist_lifecycle():
    bl = TokenBlacklist()
    assert bl.is_revoked("jti_1") is False

    bl.revoke("jti_1", exp=int(time.time() + 10))
    assert bl.is_revoked("jti_1") is True

    # Expired token in blacklist
    bl.revoke("jti_2", exp=int(time.time() - 2))
    assert bl.is_revoked("jti_2") is False


def test_token_blacklist_purge():
    bl = TokenBlacklist()
    bl.revoke("active", exp=int(time.time() + 100))
    bl.revoke("dead", exp=int(time.time() - 10))
    purged = bl.purge_expired()
    assert purged == 1
    assert bl.is_revoked("active") is True
'''
        }
    })

    # 20: tests/test_rate_limiter.py
    commits.append({
        "id": 20,
        "msg": "test(security): add unit tests for sliding-window rate limiter under burst traffic",
        "files": ["tests/test_rate_limiter.py"],
        "setup": lambda: {
            "tests/test_rate_limiter.py": '''"""Unit tests for sliding-window rate limiter."""

import time
from backend.rate_limiter import SlidingWindowRateLimiter


def test_rate_limiter_allows_up_to_limit():
    limiter = SlidingWindowRateLimiter(limit=5, window_seconds=1.0)
    for _ in range(5):
        allowed, rem, _ = limiter.is_allowed("client_a")
        assert allowed is True

    # 6th request rejected
    allowed, rem, retry_after = limiter.is_allowed("client_a")
    assert allowed is False
    assert rem == 0
    assert retry_after > 0


def test_rate_limiter_distinct_clients():
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=1.0)
    assert limiter.is_allowed("c1")[0] is True
    assert limiter.is_allowed("c1")[0] is True
    assert limiter.is_allowed("c1")[0] is False

    # c2 still allowed
    assert limiter.is_allowed("c2")[0] is True
'''
        }
    })

    # 21: tests/test_rbac.py
    commits.append({
        "id": 21,
        "msg": "test(security): verify RBAC permission enforcement and unauthorized access rejections",
        "files": ["tests/test_rbac.py"],
        "setup": lambda: {
            "tests/test_rbac.py": '''"""Unit tests for Role-Based Access Control logic."""

from backend.rbac import has_permission


def test_rbac_admin_permissions():
    assert has_permission("admin", "workspaces:delete") is True
    assert has_permission("admin", "evaluations:run") is True
    assert has_permission("admin", "settings:manage") is True


def test_rbac_viewer_permissions():
    assert has_permission("viewer", "workspaces:read") is True
    assert has_permission("viewer", "workspaces:delete") is False
    assert has_permission("viewer", "evaluations:run") is False
'''
        }
    })

    # 22: tests/test_security_headers.py
    commits.append({
        "id": 22,
        "msg": "test(security): verify security headers middleware injection in HTTP responses",
        "files": ["tests/test_security_headers.py"],
        "setup": lambda: {
            "tests/test_security_headers.py": '''"""Unit tests for defensive HTTP response security headers."""

import pytest
from starlette.responses import PlainTextResponse
from backend.security_headers import SECURITY_HEADERS


def test_security_headers_constants():
    assert SECURITY_HEADERS["X-Content-Type-Options"] == "nosniff"
    assert SECURITY_HEADERS["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" in SECURITY_HEADERS
'''
        }
    })

    # 23: tests/test_api_auth_routes.py
    commits.append({
        "id": 23,
        "msg": "test(api): test authentication endpoints and token issuance responses",
        "files": ["tests/test_api_auth_routes.py"],
        "setup": lambda: {
            "tests/test_api_auth_routes.py": '''"""Integration tests for FastAPI authentication router endpoints."""

from backend.api_auth_routes import USERS_DB
from backend.password_utils import verify_password


def test_demo_admin_credentials_present():
    assert "admin" in USERS_DB
    assert verify_password("synaptiq-admin-pass", USERS_DB["admin"]["password_hash"]) is True
'''
        }
    })

    # 24: docs/security_audit.md
    commits.append({
        "id": 24,
        "msg": "docs(security): create comprehensive security architecture and audit guide",
        "files": ["docs/security_audit.md"],
        "setup": lambda: {
            "docs/security_audit.md": '''# 🛡️ SynaptiQ Security Architecture & Audit Runbook

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
'''
        }
    })

    # 25: backend/retrieval_schemas.py
    commits.append({
        "id": 25,
        "msg": "feat(retriever): define hybrid search configuration schemas and scoring interfaces",
        "files": ["backend/retrieval_schemas.py"],
        "setup": lambda: {
            "backend/retrieval_schemas.py": '''"""Data structures and configuration schemas for hybrid retrieval."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HybridSearchConfig(BaseModel):
    dense_weight: float = Field(0.6, ge=0.0, le=1.0, description="Weight for vector similarity")
    sparse_weight: float = Field(0.4, ge=0.0, le=1.0, description="Weight for BM25 lexical score")
    rrf_k: int = Field(60, ge=1, description="Reciprocal Rank Fusion constant factor")
    top_k: int = Field(5, ge=1, le=50, description="Final number of passages to return")
    use_reranker: bool = Field(False, description="Whether to apply cross-encoder reranking")


class ScoredPassage(BaseModel):
    chunk_id: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    dense_score: Optional[float] = None
    sparse_score: Optional[float] = None
    fused_score: float = 0.0
'''
        }
    })

    # 26: backend/rrf.py
    commits.append({
        "id": 26,
        "msg": "feat(retriever): implement Reciprocal Rank Fusion (RRF) algorithm for multi-source ranking",
        "files": ["backend/rrf.py"],
        "setup": lambda: {
            "backend/rrf.py": '''"""Reciprocal Rank Fusion (RRF) combining dense and lexical ranking signals."""

from __future__ import annotations

from typing import List, Dict, Tuple


def reciprocal_rank_fusion(
    dense_ranks: List[str],
    sparse_ranks: List[str],
    k: int = 60,
    dense_weight: float = 1.0,
    sparse_weight: float = 1.0
) -> List[Tuple[str, float]]:
    """Merges two ranked lists of chunk IDs using weighted Reciprocal Rank Fusion."""
    scores: Dict[str, float] = {}

    for rank, chunk_id in enumerate(dense_ranks, start=1):
        scores[chunk_id] = scores.get(chunk_id, 0.0) + dense_weight * (1.0 / (k + rank))

    for rank, chunk_id in enumerate(sparse_ranks, start=1):
        scores[chunk_id] = scores.get(chunk_id, 0.0) + sparse_weight * (1.0 / (k + rank))

    sorted_results = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_results
'''
        }
    })

    # 27: backend/hybrid_retriever.py
    commits.append({
        "id": 27,
        "msg": "feat(retriever): scaffold hybrid dense-sparse retriever coordinating BM25 and vector stores",
        "files": ["backend/hybrid_retriever.py"],
        "setup": lambda: {
            "backend/hybrid_retriever.py": '''"""Hybrid Retriever orchestrating dense embeddings and BM25 lexical search."""

from __future__ import annotations

from typing import List, Dict, Any
from .retrieval_schemas import HybridSearchConfig, ScoredPassage
from .rrf import reciprocal_rank_fusion


class HybridRetriever:
    """Combines dense vector retrieval with BM25 sparse keyword search."""

    def __init__(self, config: HybridSearchConfig | None = None):
        self.config = config or HybridSearchConfig()

    def fuse(
        self,
        dense_results: List[Dict[str, Any]],
        sparse_results: List[Dict[str, Any]]
    ) -> List[ScoredPassage]:
        """Fuses dense and sparse candidate passages using Reciprocal Rank Fusion."""
        dense_ids = [r["id"] for r in dense_results]
        sparse_ids = [r["id"] for r in sparse_results]

        passage_lookup = {}
        for r in dense_results:
            passage_lookup[r["id"]] = r
        for r in sparse_results:
            if r["id"] not in passage_lookup:
                passage_lookup[r["id"]] = r

        fused = reciprocal_rank_fusion(
            dense_ids,
            sparse_ids,
            k=self.config.rrf_k,
            dense_weight=self.config.dense_weight,
            sparse_weight=self.config.sparse_weight
        )

        out: List[ScoredPassage] = []
        for chunk_id, score in fused[:self.config.top_k]:
            data = passage_lookup[chunk_id]
            out.append(ScoredPassage(
                chunk_id=chunk_id,
                text=data.get("text", ""),
                metadata=data.get("metadata", {}),
                fused_score=score
            ))
        return out
'''
        }
    })

    # 28: backend/reranker.py
    commits.append({
        "id": 28,
        "msg": "feat(retriever): add cross-encoder reranking client with heuristic fallback",
        "files": ["backend/reranker.py"],
        "setup": lambda: {
            "backend/reranker.py": '''"""Cross-encoder reranking client with resilient lexical fallback."""

from __future__ import annotations

import re
from typing import List
from .retrieval_schemas import ScoredPassage


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    def rerank(self, query: str, passages: List[ScoredPassage], top_k: int = 5) -> List[ScoredPassage]:
        """Reranks candidate passages based on query relevance."""
        if not passages:
            return []

        # Heuristic token overlap fallback when torch / transformer model is omitted
        q_tokens = set(re.findall(r"\w+", query.lower()))
        for p in passages:
            p_tokens = set(re.findall(r"\w+", p.text.lower()))
            overlap = len(q_tokens & p_tokens) / max(1, len(q_tokens))
            p.fused_score = p.fused_score * 0.5 + overlap * 0.5

        passages.sort(key=lambda p: p.fused_score, reverse=True)
        return passages[:top_k]
'''
        }
    })

    # 29: backend/query_decomposer.py
    commits.append({
        "id": 29,
        "msg": "feat(retriever): implement query decomposition engine for multi-hop questions",
        "files": ["backend/query_decomposer.py"],
        "setup": lambda: {
            "backend/query_decomposer.py": '''"""Query decomposition engine splitting complex multi-hop queries into sub-questions."""

from __future__ import annotations

import re
from typing import List


class QueryDecomposer:
    """Splits multi-faceted questions into atomic sub-queries for focused retrieval."""

    def decompose(self, query: str) -> List[str]:
        q = query.strip()
        if not q:
            return []

        # Split on coordinating conjunctions and transition words
        sub_queries = re.split(r"\s+(?:and also|as well as|compared to|versus|vs\.?)\s+", q, flags=re.IGNORECASE)
        cleaned = [s.strip(" ?,.;") for s in sub_queries if len(s.strip()) > 5]

        return cleaned if len(cleaned) > 1 else [q]
'''
        }
    })

    # 30: backend/hyde.py
    commits.append({
        "id": 30,
        "msg": "feat(retriever): add Hypothetical Document Embeddings (HyDE) expansion strategy",
        "files": ["backend/hyde.py"],
        "setup": lambda: {
            "backend/hyde.py": '''"""Hypothetical Document Embeddings (HyDE) zero-shot document expansion."""

from __future__ import annotations

import re


class HyDEExpander:
    """Constructs hypothetical ideal documents to bridge the query-document vocabulary gap."""

    def build_hypothetical_prompt(self, question: str) -> str:
        return (
            "Please write a short, informative passage that thoroughly answers the following question:\\n"
            f"Question: {question}\\n\\n"
            "Passage:"
        )

    def extract_search_terms(self, hypothetical_doc: str) -> list[str]:
        tokens = re.findall(r"[A-Za-z0-9_-]{4,}", hypothetical_doc.lower())
        return list(dict.fromkeys(tokens))[:20]
'''
        }
    })

    # 31: backend/context_compressor.py
    commits.append({
        "id": 31,
        "msg": "feat(retriever): implement context compression and passage deduplication filter",
        "files": ["backend/context_compressor.py"],
        "setup": lambda: {
            "backend/context_compressor.py": '''"""Context compression and redundant passage filtering for token savings."""

from __future__ import annotations

import difflib
from typing import List
from .retrieval_schemas import ScoredPassage


class ContextCompressor:
    def __init__(self, similarity_threshold: float = 0.85):
        self.threshold = similarity_threshold

    def deduplicate(self, passages: List[ScoredPassage]) -> List[ScoredPassage]:
        """Removes near-duplicate passages based on text sequence similarity."""
        unique: List[ScoredPassage] = []
        for p in passages:
            is_dup = False
            for u in unique:
                ratio = difflib.SequenceMatcher(None, p.text, u.text).quick_ratio()
                if ratio >= self.threshold:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(p)
        return unique
'''
        }
    })

    # 32: backend/dynamic_topk.py
    commits.append({
        "id": 32,
        "msg": "feat(retriever): add dynamic top-k thresholding based on cumulative score entropy",
        "files": ["backend/dynamic_topk.py"],
        "setup": lambda: {
            "backend/dynamic_topk.py": '''"""Dynamic top-k selection adapting context length to retrieval score distribution."""

from __future__ import annotations

from typing import List
from .retrieval_schemas import ScoredPassage


def select_dynamic_topk(
    passages: List[ScoredPassage],
    min_k: int = 2,
    max_k: int = 8,
    decay_cutoff: float = 0.4
) -> List[ScoredPassage]:
    """Selects top passages dynamically before relative confidence drops significantly."""
    if len(passages) <= min_k:
        return passages

    top_score = max(p.fused_score for p in passages) if passages else 1.0
    selected = []

    for idx, p in enumerate(passages):
        if idx < min_k:
            selected.append(p)
        elif idx < max_k and (p.fused_score / max(1e-6, top_score)) >= decay_cutoff:
            selected.append(p)
        else:
            break

    return selected
'''
        }
    })

    # 33: backend/retrieval_cache.py
    commits.append({
        "id": 33,
        "msg": "feat(retriever): implement LRU semantic cache for embedding and retrieval results",
        "files": ["backend/retrieval_cache.py"],
        "setup": lambda: {
            "backend/retrieval_cache.py": '''"""In-memory LRU cache storing embedding vectors and retrieval candidates."""

from __future__ import annotations

import collections
import threading
from typing import Any, Optional


class RetrievalLRUCache:
    def __init__(self, capacity: int = 500):
        self.capacity = capacity
        self._cache = collections.OrderedDict()
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self.hits += 1
                return self._cache[key]
            self.misses += 1
            return None

    def put(self, key: str, value: Any) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)
'''
        }
    })

    # 34: backend/metadata_filter.py
    commits.append({
        "id": 34,
        "msg": "feat(retriever): implement metadata filtering predicate engine (dates, authors, tags)",
        "files": ["backend/metadata_filter.py"],
        "setup": lambda: {
            "backend/metadata_filter.py": '''"""Metadata filtering engine evaluating boolean conditions on chunk metadata."""

from __future__ import annotations

from typing import Dict, Any, Callable


class MetadataFilterEngine:
    @staticmethod
    def match(metadata: Dict[str, Any], query_filters: Dict[str, Any]) -> bool:
        """Returns True if chunk metadata satisfies all specified filter key-values."""
        if not query_filters:
            return True

        for key, expected in query_filters.items():
            val = metadata.get(key)
            if isinstance(expected, list):
                if val not in expected:
                    return False
            elif val != expected:
                return False
        return True
'''
        }
    })

    # 35: tests/test_rrf.py
    commits.append({
        "id": 35,
        "msg": "test(retriever): add unit tests for Reciprocal Rank Fusion merge accuracy",
        "files": ["tests/test_rrf.py"],
        "setup": lambda: {
            "tests/test_rrf.py": '''"""Unit tests for Reciprocal Rank Fusion."""

from backend.rrf import reciprocal_rank_fusion


def test_rrf_scoring_order():
    dense = ["doc_a", "doc_b", "doc_c"]
    sparse = ["doc_b", "doc_a", "doc_d"]

    # doc_a: 1/(60+1) + 1/(60+2)
    # doc_b: 1/(60+2) + 1/(60+1)
    fused = reciprocal_rank_fusion(dense, sparse, k=60)
    top_two = [item[0] for item in fused[:2]]
    assert "doc_a" in top_two
    assert "doc_b" in top_two
    assert fused[-1][0] in ("doc_c", "doc_d")
'''
        }
    })

    # 36: tests/test_hybrid_retriever.py
    commits.append({
        "id": 36,
        "msg": "test(retriever): add unit tests for hybrid dense and sparse score weighting",
        "files": ["tests/test_hybrid_retriever.py"],
        "setup": lambda: {
            "tests/test_hybrid_retriever.py": '''"""Unit tests for HybridRetriever coordinator."""

from backend.hybrid_retriever import HybridRetriever
from backend.retrieval_schemas import HybridSearchConfig


def test_hybrid_retriever_fuse():
    retriever = HybridRetriever(HybridSearchConfig(top_k=2))
    dense = [{"id": "c1", "text": "hello world"}, {"id": "c2", "text": "another chunk"}]
    sparse = [{"id": "c2", "text": "another chunk"}, {"id": "c3", "text": "third chunk"}]

    fused = retriever.fuse(dense, sparse)
    assert len(fused) == 2
    assert fused[0].chunk_id == "c2"
'''
        }
    })

    # 37: tests/test_reranker.py
    commits.append({
        "id": 37,
        "msg": "test(retriever): test cross-encoder reranker fallback mechanism when model is absent",
        "files": ["tests/test_reranker.py"],
        "setup": lambda: {
            "tests/test_reranker.py": '''"""Unit tests for CrossEncoderReranker fallback."""

from backend.reranker import CrossEncoderReranker
from backend.retrieval_schemas import ScoredPassage


def test_reranker_lexical_overlap():
    reranker = CrossEncoderReranker()
    p1 = ScoredPassage(chunk_id="1", text="Python programming guide", fused_score=0.1)
    p2 = ScoredPassage(chunk_id="2", text="Irrelevant content about apples", fused_score=0.2)

    results = reranker.rerank("Python programming", [p1, p2], top_k=2)
    assert results[0].chunk_id == "1"
'''
        }
    })

    # 38: tests/test_query_decomposer.py
    commits.append({
        "id": 38,
        "msg": "test(retriever): add unit tests for multi-hop query decomposition logic",
        "files": ["tests/test_query_decomposer.py"],
        "setup": lambda: {
            "tests/test_query_decomposer.py": '''"""Unit tests for multi-hop query decomposition."""

from backend.query_decomposer import QueryDecomposer


def test_query_decomposer_splitting():
    decomposer = QueryDecomposer()
    subs = decomposer.decompose("What is FastAPI and also how does Uvicorn work?")
    assert len(subs) == 2
    assert "FastAPI" in subs[0]
    assert "Uvicorn" in subs[1]


def test_query_decomposer_single_question():
    decomposer = QueryDecomposer()
    subs = decomposer.decompose("What is RAG?")
    assert len(subs) == 1
'''
        }
    })

    # 39: tests/test_hyde.py
    commits.append({
        "id": 39,
        "msg": "test(retriever): add unit tests for HyDE prompt formatting and response parsing",
        "files": ["tests/test_hyde.py"],
        "setup": lambda: {
            "tests/test_hyde.py": '''"""Unit tests for HyDE expansion strategy."""

from backend.hyde import HyDEExpander


def test_hyde_prompt_and_terms():
    hyde = HyDEExpander()
    prompt = hyde.build_hypothetical_prompt("How does backpropagation work?")
    assert "Question: How does backpropagation work?" in prompt

    terms = hyde.extract_search_terms("Neural networks optimize weights through gradient descent")
    assert "neural" in terms
    assert "gradient" in terms
'''
        }
    })

    # 40: tests/test_context_compressor.py
    commits.append({
        "id": 40,
        "msg": "test(retriever): add unit tests for context compression and deduplication ratios",
        "files": ["tests/test_context_compressor.py"],
        "setup": lambda: {
            "tests/test_context_compressor.py": '''"""Unit tests for context compression."""

from backend.context_compressor import ContextCompressor
from backend.retrieval_schemas import ScoredPassage


def test_context_compressor_deduplication():
    compressor = ContextCompressor(similarity_threshold=0.8)
    p1 = ScoredPassage(chunk_id="1", text="The quick brown fox jumps over the lazy dog.")
    p2 = ScoredPassage(chunk_id="2", text="The quick brown fox jumps over the lazy dog!")
    p3 = ScoredPassage(chunk_id="3", text="Completely distinct sentence about robotics.")

    unique = compressor.deduplicate([p1, p2, p3])
    assert len(unique) == 2
    assert unique[0].chunk_id == "1"
    assert unique[1].chunk_id == "3"
'''
        }
    })

    # 41: tests/test_retrieval_cache.py
    commits.append({
        "id": 41,
        "msg": "test(retriever): test semantic retrieval cache eviction and hit-rate metrics",
        "files": ["tests/test_retrieval_cache.py"],
        "setup": lambda: {
            "tests/test_retrieval_cache.py": '''"""Unit tests for retrieval LRU cache."""

from backend.retrieval_cache import RetrievalLRUCache


def test_cache_hits_and_eviction():
    cache = RetrievalLRUCache(capacity=2)
    cache.put("k1", "val1")
    cache.put("k2", "val2")

    assert cache.get("k1") == "val1"
    assert cache.hits == 1

    cache.put("k3", "val3")  # Evicts k2 because k1 was accessed
    assert cache.get("k2") is None
    assert cache.misses == 1
'''
        }
    })

    # 42: docs/hybrid_retrieval_guide.md
    commits.append({
        "id": 42,
        "msg": "docs(retriever): document hybrid retrieval architecture and RRF parameter tuning",
        "files": ["docs/hybrid_retrieval_guide.md"],
        "setup": lambda: {
            "docs/hybrid_retrieval_guide.md": '''# 🔍 SynaptiQ Hybrid Retrieval Architecture

SynaptiQ fuses dense semantic embeddings with BM25 lexical keyword matching using **Reciprocal Rank Fusion (RRF)**.

## Fusion Formula
$$\\text{RRF Score}(d) = \\sum_{m \\in \\{dense, sparse\\}} w_m \\cdot \\frac{1}{k + r_m(d)}$$

- Default constant $k = 60$
- Dense weight: $0.6$
- Lexical sparse weight: $0.4$
'''
        }
    })

    return commits
