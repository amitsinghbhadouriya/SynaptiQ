"""Shared Streamlit helpers: the cached workspace, page paths and full-screen styling."""

from __future__ import annotations

import streamlit as st

from backend.process_lock import StorageInUse
from backend.service import Workspace

HOME = "streamlit_ui/pages/home.py"
DASHBOARD = "streamlit_ui/pages/dashboard.py"
WORKBENCH = "streamlit_ui/pages/workbench.py"
TERMINAL = "streamlit_ui/pages/terminal_page.py"
PAGES = {"home": HOME, "dashboard": DASHBOARD, "workbench": WORKBENCH, "terminal": TERMINAL}


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


# Hide Streamlit's chrome and let the component iframe fill the viewport. The React app
# scrolls inside its own iframe, which is what its scroll-driven animations listen to.
FULLSCREEN_CSS = """
<style>
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
#MainMenu, footer { display: none !important; }
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background: #07080b !important; overflow: hidden !important;
}
[data-testid="stMainBlockContainer"], .block-container, [data-testid="stMain"] > div {
  padding: 0 !important; margin: 0 !important; max-width: 100% !important;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stElementContainer"]:has(style) { display: none !important; }
iframe[title*="synaptiq_ui"], iframe[data-testid="stCustomComponentV1"] {
  display: block; width: 100vw !important; height: 100vh !important; border: 0;
  overflow: auto !important;
}
</style>
"""


def fullscreen() -> None:
    st.markdown(FULLSCREEN_CSS, unsafe_allow_html=True)


def go(page: str | None) -> None:
    if page in PAGES:
        st.switch_page(PAGES[page])
