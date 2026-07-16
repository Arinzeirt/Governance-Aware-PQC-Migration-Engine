import sys
from pathlib import Path

import streamlit as st

from components.assessment_runner import run_assessment
from components.soc_header import show_header
from components.soc_pipeline import show_pipeline
from components.soc_events import show_events

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from assessment_service import service


def show_progress():

    header = st.empty()
    body = st.empty()
    footer = st.empty()

    for state in run_assessment():

        with header.container():

            show_header(
                state["session"],
                state["progress"]
            )

        with body.container():

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

    with footer.container():

        st.success("✅ Assessment Complete")

        st.info("Runtime State (Debug Mode)")

        runtime = service.get_state()

        st.json(runtime)

        if st.button("Continue to Executive Dashboard"):

            st.session_state.screen = "summary"

            st.rerun()
