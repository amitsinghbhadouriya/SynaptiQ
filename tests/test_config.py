"""Unit tests for configuration validation."""

from backend.config import get_settings


def test_settings_load():
    settings = get_settings()
    assert settings is not None
