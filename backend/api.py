"""FastAPI service: REST API for SynaptiQ plus the built website.

Run with:  uvicorn backend.api:app --reload
Docs:      http://localhost:8000/docs
Website:   http://localhost:8000/  (landing page + dashboard, served from frontend/dist)

Add authentication, HTTPS and rate limiting before exposing this beyond localhost.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any, Literal

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import __version__
from .config import PROJECT_ROOT
from .document_loader import DocumentLoadError
from .experiments import IncompatibleRuns
from .process_lock import StorageInUse
from .schemas import MODES, QUESTION_TYPES, EvaluationRun, new_id, to_jsonable
from .service import NotFound, Workspace
from .ui_bridge import build_state, handle_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("synaptiq.api")

_workspace: Workspace | None = None
_workspace_lock = threading.Lock()


def workspace() -> Workspace:
    global _workspace
    with _workspace_lock:
        if _workspace is None:
            try:
                _workspace = Workspace()
            except StorageInUse as exc:
                raise HTTPException(503, str(exc)) from exc
            _workspace.status()  # loads the embedding model once, up front
    return _workspace


def _warm_up() -> None:
    try:
        workspace()
    except HTTPException as exc:
        log.error("%s", exc.detail)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Warm up in the background so the server accepts requests immediately.
    threading.Thread(target=_warm_up, name="synaptiq-warmup", daemon=True).start()
    yield


app = FastAPI(
    title="SynaptiQ API",
    version=__version__,
    description="RAG evaluation, root-cause intelligence and optimization.",
    lifespan=lifespan,
)
