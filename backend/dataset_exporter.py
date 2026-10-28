"""Exports generated synthetic QA test datasets to JSONL."""

from __future__ import annotations

import json
from typing import List
from .qa_schemas import GeneratedQAPair


class DatasetExporter:
    @staticmethod
    def to_jsonl(qa_pairs: List[GeneratedQAPair]) -> str:
        lines = [
            json.dumps(pair.model_dump() if hasattr(pair, "model_dump") else pair.dict())
            for pair in qa_pairs
        ]
        return "\n".join(lines)
