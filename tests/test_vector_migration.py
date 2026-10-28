"""Unit tests for vector backup utility."""

import tempfile
from scripts.vector_store_migration import backup_vector_store


def test_backup_vector_store():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
        assert backup_vector_store(src, dst) is True
