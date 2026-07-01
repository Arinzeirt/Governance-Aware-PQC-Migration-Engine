import time
import streamlit as st


def show_summary():

    st.success("Assessment Completed")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Assets Analysed", 42)

    with col2:
        st.metric("High Priority", 8)

    with col3:
        st.metric("Migration Readiness", "74%")

    st.divider()

    st.info("Preparing Executive Command Center...")

    time.sleep(3)

    st.session_state.screen = "command_center"

    st.rerun()
