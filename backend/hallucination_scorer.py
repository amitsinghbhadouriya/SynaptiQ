"""Hallucination severity index quantifying unsupported proposition density."""

from __future__ import annotations

from typing import List, Dict, Any
from .attribution_schemas import AtomicClaim


def calculate_hallucination_index(claims: List[AtomicClaim]) -> Dict[str, Any]:
    if not claims:
        return {"hallucination_rate": 0.0, "risk_level": "LOW", "unsupported_count": 0}

    unsupported = sum(1 for c in claims if not c.is_supported)
    rate = unsupported / len(claims)

    if rate >= 0.5:
        level = "CRITICAL"
    elif rate >= 0.25:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "hallucination_rate": round(rate, 4),
        "risk_level": level,
        "unsupported_count": unsupported,
        "total_claims": len(claims)
    }
