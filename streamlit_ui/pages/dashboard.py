"""Dashboard page: the React dashboard, driven by Python.

Each UI action arrives as the component's value. It is applied *before* the component is
rendered (read from session state), so this same script run already sends the updated
state back — no extra rerun needed.
"""

import streamlit as st

from backend.ui_bridge import build_state, handle_event
from streamlit_ui.component import synaptiq_ui
from streamlit_ui.shared import fullscreen, get_workspace, go

KEY = "dashboard_ui"

fullscreen()
workspace = get_workspace()


def process(event: dict) -> None:
    st.session_state["dashboard_nonce"] = event.get("nonce")
    outcome = handle_event(workspace, event)
    if outcome.get("navigate"):
        go(outcome["navigate"])
    if outcome.get("selected_run_id"):
        st.session_state["selected_run_id"] = outcome["selected_run_id"]
