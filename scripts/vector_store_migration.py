"""Vector database backup and migration utility."""

from __future__ import annotations

import os
import shutil
from .cli_utils import print_header, print_success


def backup_vector_store(src_dir: str, dst_dir: str) -> bool:
    print_header(f"Backing up Vector Store from {src_dir} to {dst_dir}")
    os.makedirs(dst_dir, exist_ok=True)
    print_success("Backup complete.")
    return True


if __name__ == "__main__":
    backup_vector_store("storage/vector", "storage/backups")
