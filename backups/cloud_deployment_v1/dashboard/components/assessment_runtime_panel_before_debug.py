import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from assessment_service import service


def show_assessment_runtime(state):

    st.subheader("Assessment Runtime")

    st.progress(state["progress"] / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Current Stage",
            state["stage"]
        )

    with col2:
        st.metric(
            "Progress",
            f'{state["progress"]}%'
        )

    st.divider()

    st.markdown("### Recent Events")

    logs = state.get("logs", [])

    if logs:
        for event in logs:
            st.write(f"• {event}")
    else:
        st.info("Waiting for assessment to start...")

    st.divider()

    if state["running"]:

        if st.button(
            "▶ Next Stage",
            type="primary",
            use_container_width=True
        ):

            service.next_step()

            st.session_state.app["assessment"]["state"] = service.get_state()
            st.session_state.app["assessment"]["running"] = service.running
            st.session_state.app["assessment"]["complete"] = service.complete

            st.rerun()
