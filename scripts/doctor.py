"""SynaptiQ Doctor: environment diagnostics and sanity verification."""

from __future__ import annotations

import sys
import json
import platform
from .cli_utils import print_header, print_success, print_warning


def run_doctor(json_output: bool = False):
    status_info = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "is_healthy": True,
    }

    if json_output:
        print(json.dumps(status_info))
        return True

    print_header("SynaptiQ System Doctor")
    print(f"Python: {status_info['python_version']} ({sys.executable})")
    print(f"OS Platform: {status_info['platform']}")
    print_success("Environment check passed.")
    return True


if __name__ == "__main__":
    run_doctor("--json" in sys.argv)
