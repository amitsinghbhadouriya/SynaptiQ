"""Unit tests for premise entailment checker."""

from backend.entailment_checker import EntailmentChecker


def test_entailment_supported():
    premise = "Python 3.11 provides substantial performance improvements over 3.10."
    claim = "Python 3.11 offers performance improvements."
    supported, score = EntailmentChecker.verify_support(premise, claim)
    assert supported is True
    assert score > 0.6


def test_entailment_unsupported():
    premise = "The moon orbits the Earth."
    claim = "Jupiter has rings of liquid nitrogen."
    supported, score = EntailmentChecker.verify_support(premise, claim)
    assert supported is False
    assert score < 0.2
