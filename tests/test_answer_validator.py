"""Unit tests for answer validation."""

from backend.answer_validator import AnswerValidator


def test_answer_validator_checks():
    assert AnswerValidator.is_valid("What is SynaptiQ?", "SynaptiQ is a diagnostic platform.") is True
    assert AnswerValidator.is_valid("short", "ans") is False
    assert AnswerValidator.is_valid("Duplicate text", "Duplicate text") is False
