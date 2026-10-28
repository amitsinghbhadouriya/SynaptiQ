"""Integration tests for telemetry router."""

from backend.system_monitor import get_system_health


def test_health_check_payload():
    data = get_system_health()
    assert data["status"] == "healthy"
