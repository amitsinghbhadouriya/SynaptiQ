import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.config import load_settings  # noqa: E402
from backend.service import Workspace  # noqa: E402

SAMPLE = ROOT / "data" / "sample_docs" / "lumen_labs_handbook.txt"


@pytest.fixture
def settings(tmp_path):
    # Fast, offline and deterministic: hashing embeddings, in-memory vectors, extractive generator.
    return load_settings().with_overrides(
        embedding_backend="hashing",
        vector_backend="memory",
        llm_provider="offline",
        db_path=tmp_path / "synaptiq.db",
        chroma_path=tmp_path / "chroma",
        upload_dir=tmp_path / "uploads",
        reports_dir=tmp_path / "reports",
    )


@pytest.fixture
def workspace(settings):
    return Workspace(settings)


@pytest.fixture
def sample_bytes():
    return SAMPLE.read_bytes()


@pytest.fixture
def demo(workspace):
    return workspace.load_demo()
