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
    path = (directory.parent / f".{directory.name}.lock").resolve()
    key = str(path)
    if key in _HELD:  # already held by this process
        return
    handle = open(path, "a+")
    try:
        if sys.platform == "win32":
            import msvcrt

            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        handle.close()
        raise StorageInUse(
            f"Another SynaptiQ process (the Streamlit app or the FastAPI server) is already using {directory}. "
            "Stop the other process, or give this one its own storage with CHROMA_PATH and DB_PATH."
        ) from exc
    _HELD[key] = handle  # kept open (and locked) for the life of the process
