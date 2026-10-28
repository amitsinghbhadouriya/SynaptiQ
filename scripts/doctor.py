"""SynaptiQ Doctor: environment diagnostics and sanity verification."""

from __future__ import annotations

import sys
import platform
from .cli_utils import print_header, print_success, print_warning


def run_doctor():
    print_header("SynaptiQ System Doctor")
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    print(f"OS Platform: {platform.platform()}")

    if sys.version_info < (3, 10):
        print_warning("Python >= 3.10 is strongly recommended.")
    else:
        print_success("Python runtime version supported.")

    print_success("Environment check passed.")
    return True


if __name__ == "__main__":
    run_doctor()
