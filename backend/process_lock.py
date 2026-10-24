"""One process per storage folder.

ChromaDB's local persistent store is not designed to be shared by several processes (for
example the Streamlit app and the FastAPI server pointed at the same folder). This
non-blocking file lock makes a second process stop immediately with an explained error.
"""

from __future__ import annotations

import sys
from pathlib import Path

_HELD: dict[str, object] = {}


class StorageInUse(RuntimeError):
    pass


def acquire(directory: Path) -> None:
    directory.parent.mkdir(parents=True, exist_ok=True)
