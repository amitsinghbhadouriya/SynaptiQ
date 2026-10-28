"""Unit tests for report generator CLI."""

from scripts.generate_report import generate_markdown_report


def test_generate_markdown_report():
    rep = generate_markdown_report("run_123", 0.95)
    assert "run_123" in rep
    assert "0.95" in rep
