"""Unit tests for dataset export to JSONL."""

import json
from backend.dataset_exporter import DatasetExporter
from backend.qa_schemas import GeneratedQAPair


def test_dataset_exporter_to_jsonl():
    pair = GeneratedQAPair(question_id="q1", question="Q?", expected_answer="A", source_chunk_id="c1")
    jsonl = DatasetExporter.to_jsonl([pair])
    decoded = json.loads(jsonl)
    assert decoded["question_id"] == "q1"
