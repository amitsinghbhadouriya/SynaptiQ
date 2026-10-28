"""Pydantic schemas for structured telemetry events and latency records."""

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class TelemetryEvent(BaseModel):
    event_name: str
    timestamp: float
    trace_id: Optional[str] = None
    workspace_id: Optional[str] = None
    duration_ms: float = 0.0
    attributes: Dict[str, Any] = Field(default_factory=dict)
