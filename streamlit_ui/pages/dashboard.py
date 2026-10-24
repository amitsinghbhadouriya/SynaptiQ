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
    if event.get("type") == "compare" and outcome.get("comparison"):
        st.session_state["comparison_override"] = (outcome["comparison"], outcome.get("comparison_chart"))
    elif event.get("type") in {"select_run", "run_eval", "run_candidate", "load_demo", "delete_document"}:
        st.session_state.pop("comparison_override", None)
    st.session_state["dashboard_outcome"] = outcome


def is_new(event) -> bool:
    return bool(event) and event.get("nonce") != st.session_state.get("dashboard_nonce")


pending = st.session_state.get(KEY)
if is_new(pending):
    process(pending)

state = build_state(workspace, st.session_state.get("selected_run_id"))
outcome = st.session_state.get("dashboard_outcome") or {}
state["notice"] = outcome.get("notice")
state["download"] = outcome.get("download")
override = st.session_state.get("comparison_override")
if override:
    state["comparison"], state["charts"]["comparison"] = override

event = synaptiq_ui(view="dashboard", data=state, key=KEY)
if is_new(event):  # fallback if the value was not yet visible in session state
    process(event)
    st.rerun()
