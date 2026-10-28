"""Unit tests for JSON log formatter."""

import json
import logging
from backend.json_logger import JSONFormatter


def test_json_formatter_output():
    formatter = JSONFormatter()
    record = logging.LogRecord("test", logging.INFO, "test.py", 10, "Hello log", (), None)
    record.trace_id = "trace_123"
    formatted = formatter.format(record)
    data = json.loads(formatted)
    assert data["message"] == "Hello log"
    assert data["level"] == "INFO"
    assert data["trace_id"] == "trace_123"
