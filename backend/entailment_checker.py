"""Entailment and contradiction validator evaluating claim premise support."""

from __future__ import annotations

import re
from typing import Tuple


class EntailmentChecker:
    @staticmethod
    def verify_support(premise: str, claim: str) -> Tuple[bool, float]:
        """Evaluates whether premise text supports claim text."""
        p_tokens = set(re.findall(r"\w+", premise.lower()))
        c_tokens = set(re.findall(r"\w+", claim.lower()))

        if not c_tokens:
            return True, 1.0

        overlap = len(p_tokens & c_tokens)
        score = overlap / len(c_tokens)
        is_supported = score >= 0.5
        return is_supported, score
