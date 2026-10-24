"""Shared Streamlit helpers: the cached workspace, page paths and full-screen styling."""

from __future__ import annotations

import streamlit as st

from backend.process_lock import StorageInUse
from backend.service import Workspace

HOME = "streamlit_ui/pages/home.py"
DASHBOARD = "streamlit_ui/pages/dashboard.py"
WORKBENCH = "streamlit_ui/pages/workbench.py"
PAGES = {"home": HOME, "dashboard": DASHBOARD, "workbench": WORKBENCH}


@st.cache_resource(show_spinner="Starting SynaptiQ — loading the embedding model…")
def _workspace() -> Workspace:
    workspace = Workspace()
    workspace.status()  # load the embedding model once per server process
    return workspace


def get_workspace() -> Workspace:
    try:
        return _workspace()
    except StorageInUse as exc:
        st.error(str(exc))
        st.stop()


