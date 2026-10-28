"""Telemetry and monitoring API routes."""

from __future__ import annotations

from fastapi import APIRouter
from .metrics_collector import metrics_collector
from .system_monitor import get_system_health

telemetry_router = APIRouter(prefix="/api/v1/telemetry", tags=["telemetry"])


@telemetry_router.get("/metrics")
async def get_metrics():
    return metrics_collector.get_summary()


@telemetry_router.get("/health")
async def get_health():
    return get_system_health()
