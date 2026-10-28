"""SynaptiQ backend: ingestion, retrieval, generation, evaluation and diagnosis."""

__version__ = "1.1.0"

from .windows_patch import patch_windows_asyncio

patch_windows_asyncio()
