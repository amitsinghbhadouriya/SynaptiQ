"""Host hardware and process resource health diagnostics."""

from __future__ import annotations

import os
import platform
import sys
from typing import Dict, Any


def get_system_health() -> Dict[str, Any]:
    return {
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "cpu_count": os.cpu_count() or 1,
        "pid": os.getpid(),
        "status": "healthy"
    }
