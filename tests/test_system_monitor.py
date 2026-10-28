"""Unit tests for system monitor."""

from backend.system_monitor import get_system_health


def test_system_health_fields():
    h = get_system_health()
    assert h["status"] == "healthy"
    assert "platform" in h
    assert "cpu_count" in h
