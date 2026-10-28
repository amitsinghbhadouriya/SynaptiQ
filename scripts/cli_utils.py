"""Command-line interface helpers, styling, and terminal formatting."""

from __future__ import annotations

import sys


def print_header(title: str) -> None:
    print(f"\n{'=' * 60}\n  {title}\n{'=' * 60}")


def print_success(msg: str) -> None:
    print(f"\033[92m[✓]\033[0m {msg}")


def print_warning(msg: str) -> None:
    print(f"\033[93m[!]\033[0m {msg}")


def print_error(msg: str) -> None:
    print(f"\033[91m[✗]\033[0m {msg}", file=sys.stderr)
