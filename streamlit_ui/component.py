"""The React landing page + dashboard (frontend/dist) as a bidirectional Streamlit component.

Python sends `view` and `data` (the dashboard state); the component sends back one UI
action at a time (upload, run, compare, navigate, ...), each tagged with a unique nonce.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

_component = components.declare_component("synaptiq_ui", path=str(DIST)) if (DIST / "index.html").is_file() else None


def synaptiq_ui(view: str, data: dict[str, Any] | None = None, key: str | None = None) -> dict[str, Any] | None:
    if _component is None:
        st.error(
            "The web UI build is missing (frontend/dist). Build it once with:\n\n"
            "`npm --prefix frontend install` and `npm --prefix frontend run build`"
        )
        return None
    return _component(view=view, data=data, key=key, default=None)
