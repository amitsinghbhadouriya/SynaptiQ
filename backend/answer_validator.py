"""Validates completeness, length, and sanity of synthetic QA ground truths."""

from __future__ import annotations


class AnswerValidator:
    @staticmethod
    def is_valid(question: str, answer: str) -> bool:
        if len(question.strip()) < 10:
            return False
        if len(answer.strip()) < 5:
            return False
        if question.lower().strip() == answer.lower().strip():
            return False
        return True
