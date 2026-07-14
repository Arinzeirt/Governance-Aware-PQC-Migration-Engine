from pathlib import Path

import streamlit as st

from engine.runner import runner
from engine.runtime import runtime


DEFAULT_REPOSITORY = str(
    Path.home()
    / "Downloads"
    / "streple-backend-main"
)


def show():

    st.markdown("## Assessment Target")

    target_type = st.radio(

        "Target Type",

        [

            "Local Directory",

            "GitHub Repository",

        ],

        horizontal=True,

    )

    if target_type == "Local Directory":

        target = st.text_input(

            "Repository Path",

            value=DEFAULT_REPOSITORY,

        )

    else:

        target = st.text_input(

            "GitHub Repository URL",

            placeholder="https://github.com/owner/repository",

        )

    st.session_state.assessment_target_type = target_type
    st.session_state.assessment_target = target

    st.write("")

    running = runner.is_running()

    if running:

        st.info("Assessment is currently running...")

    col1, col2 = st.columns([3, 1])

    with col2:

        if st.button(

            "Start Assessment",

            type="primary",

            use_container_width=True,

            disabled=running,

        ):

            started = runner.start(

                target_type,

                target,

            )

            if started:

                st.rerun()

