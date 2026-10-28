"""Unit tests for doctor diagnostic utility."""

from scripts.doctor import run_doctor


def test_doctor_execution():
    assert run_doctor() is True
