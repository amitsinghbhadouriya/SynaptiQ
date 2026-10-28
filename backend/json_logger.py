"""Structured JSON log formatter for cloud observability platforms."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if hasattr(record, "trace_id"):
            log_obj["trace_id"] = record.trace_id
        return json.dumps(log_obj)
