"""Terminal demo page: displays the Magic UI Terminal components in Streamlit."""

import streamlit as st
from streamlit_ui.terminal import render_terminal_demo, render_synaptiq_terminal
from streamlit_ui.scroll_expansion import render_scroll_expansion_demo

st.title("💻 Interactive Terminal & Components")
st.caption("Native Python Streamlit components — runs with zero node_modules or npm dependencies.")

col_nav1, col_nav2 = st.columns([1, 5])
with col_nav1:
    if st.button("← Return to Home", width="stretch"):
        st.switch_page("streamlit_ui/pages/home.py")

st.divider()

tab1, tab2, tab3 = st.tabs(["Command Line Init Demo", "SynaptiQ RAG Diagnostic", "Scroll Expansion Hero"])

with tab1:
    st.subheader("Shadcn CLI Initialization Demo")
    st.caption("Sequential typing animation with green preflight checks and status spans.")
    render_terminal_demo(height=460)

with tab2:
    st.subheader("SynaptiQ Automated Evaluation Workflow")
    st.caption("Live simulated terminal showing RAG evaluation, ChromaDB indexing, and root-cause fix verification.")
    render_synaptiq_terminal(height=460)

with tab3:
    st.subheader("Scroll Expansion Hero Demo")
    st.caption("Converted from scroll-expansion-hero.tsx into pure Python.")
    render_scroll_expansion_demo(height=650)

