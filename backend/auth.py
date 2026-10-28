"""JWT token issuance, verification, and API key authentication services."""

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
