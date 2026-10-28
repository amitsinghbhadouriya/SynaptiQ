"""Cryptographic password hashing and verification using standard PBKDF2-HMAC-SHA256."""

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
