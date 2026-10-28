"""W3C Trace Context (traceparent) parser and generator."""

from __future__ import annotations

import secrets
from typing import Optional, Tuple


def generate_trace_id() -> str:
    return secrets.token_hex(16)


def generate_span_id() -> str:
    return secrets.token_hex(8)


def parse_traceparent(header_val: str) -> Optional[Tuple[str, str]]:
    """Parses '00-{trace_id}-{span_id}-{flags}' header value."""
    try:
        parts = header_val.strip().split("-")
        if len(parts) == 4 and parts[0] == "00":
            return parts[1], parts[2]
        return None
    except Exception:
        return None
