"""Unit tests for batch evaluation CLI."""

import subprocess
import sys


def test_cli_evaluate_batch_help():
    res = subprocess.run([sys.executable, "-m", "scripts.evaluate_batch", "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "SynaptiQ Batch RAG Evaluation Runner" in res.stdout
