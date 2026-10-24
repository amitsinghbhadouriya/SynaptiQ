"""Landing page: the 3D React landing page, full screen."""

import streamlit as st

from streamlit_ui.component import synaptiq_ui
from streamlit_ui.shared import fullscreen, go

fullscreen()
event = synaptiq_ui(view="landing", key="landing_ui")

if event and event.get("nonce") != st.session_state.get("landing_nonce"):
    st.session_state["landing_nonce"] = event.get("nonce")
    if event.get("type") == "navigate":
        go(event.get("page"))
