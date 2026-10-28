"""Unit tests for defensive HTTP response security headers."""

import pytest
from starlette.responses import PlainTextResponse
from backend.security_headers import SECURITY_HEADERS


def test_security_headers_constants():
    assert SECURITY_HEADERS["X-Content-Type-Options"] == "nosniff"
    assert SECURITY_HEADERS["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" in SECURITY_HEADERS
