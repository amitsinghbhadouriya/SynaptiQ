"""Unit tests for PBKDF2 password hashing and verification."""

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
