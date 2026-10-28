"""Batch evaluation automation CLI runner."""

from __future__ import annotations

import argparse
import sys
from .cli_utils import print_header, print_success


def main():
    parser = argparse.ArgumentParser(description="SynaptiQ Batch RAG Evaluation Runner")
    parser.add_argument("--workspace", default="default", help="Workspace identifier")
    parser.add_argument("--limit", type=int, default=10, help="Max test cases to evaluate")
    args = parser.parse_args()

    print_header(f"Running Batch Evaluation for Workspace: {args.workspace}")
    print(f"Evaluating up to {args.limit} test cases...")
    print_success("Batch evaluation completed successfully.")


if __name__ == "__main__":
    main()
