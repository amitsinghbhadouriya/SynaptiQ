"""Automated mitigation recommendation generator for detected hallucinations."""

from __future__ import annotations

from typing import List


def generate_hallucination_mitigations(risk_level: str, unsupported_count: int) -> List[str]:
    mitigations = []
    if risk_level in ("CRITICAL", "HIGH"):
        mitigations.append("Lower generator temperature to 0.1 to discourage creative completion.")
        mitigations.append("Enforce strict citation-grounded prompt constraints.")
        mitigations.append("Increase top-k retrieval depth to supply more comprehensive source facts.")
    elif risk_level == "MEDIUM":
        mitigations.append("Add verification step with cross-encoder reranker before response generation.")
    else:
        mitigations.append("Generation aligns well with provided source context.")
    return mitigations
