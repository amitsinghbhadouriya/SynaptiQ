"""SynaptiQ — Streamlit entry point.

    streamlit run app.py

Pages (navigation happens inside the UI, so Streamlit's own sidebar is hidden):
  * Home       — 3D landing page (React, served as a Streamlit component)
  * Dashboard  — evaluation dashboard (React + Magic Bento), driven by Python
  * Workbench  — native Streamlit tools: uploads, test-set review, tables and Plotly charts
"""

import streamlit as st

from backend.windows_patch import patch_windows_asyncio

patch_windows_asyncio()

st.set_page_config(
    page_title="SynaptiQ — RAG evaluation",
    page_icon=":material/hub:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

pages = [
    st.Page("streamlit_ui/pages/home.py", title="Home", icon=":material/home:", url_path="home", default=True),
    st.Page("streamlit_ui/pages/dashboard.py", title="Dashboard", icon=":material/dashboard:", url_path="dashboard"),
    st.Page("streamlit_ui/pages/workbench.py", title="Workbench", icon=":material/build:", url_path="workbench"),
]

st.navigation(pages, position="hidden").run()
