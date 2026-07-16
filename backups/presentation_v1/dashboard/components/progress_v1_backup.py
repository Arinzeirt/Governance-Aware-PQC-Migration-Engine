import time
import streamlit as st

from components.assessment_runner import run_assessment
from components.soc_header import show_header
from components.soc_pipeline import show_pipeline
from components.soc_events import show_events


def show_progress():

    for state in run_assessment():

        st.empty()

        show_header(
            state["session"],
            state["progress"]
        )

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Current Operation")

            st.info(state["operation"])

            st.divider()

            show_pipeline(
                state["completed"],
                state["current"],
                state["pending"]
            )

        with right:

            show_events(
                state["log"]
            )

    st.success("Assessment Complete")

    st.info("Generating Executive Summary...")

    time.sleep(2)

    st.session_state.screen = "summary"

    st.rerun()

