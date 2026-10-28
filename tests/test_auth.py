"""Unit tests for token issuance and cryptographic verification."""

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
