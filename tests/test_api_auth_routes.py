"""Integration tests for FastAPI authentication router endpoints."""

from backend.api_auth_routes import USERS_DB
from backend.password_utils import verify_password


def test_demo_admin_credentials_present():
    assert "admin" in USERS_DB
    assert verify_password("synaptiq-admin-pass", USERS_DB["admin"]["password_hash"]) is True
