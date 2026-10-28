"""Metadata filtering engine evaluating boolean conditions on chunk metadata."""

from __future__ import annotations

from typing import Dict, Any, Callable


class MetadataFilterEngine:
    @staticmethod
    def match(metadata: Dict[str, Any], query_filters: Dict[str, Any]) -> bool:
        """Returns True if chunk metadata satisfies all specified filter key-values."""
        if not query_filters:
            return True

        for key, expected in query_filters.items():
            val = metadata.get(key)
            if isinstance(expected, list):
                if val not in expected:
                    return False
            elif val != expected:
                return False
        return True
