import streamlit as st

from engine.assessment_engine import engine
from engine.runtime import runtime


def show():

    st.markdown("## Assessment Runtime")

    #
    # Progress
    #
    st.progress(runtime.progress)

    #
    # Status
    #
    col1, col2 = st.columns([4, 1])

    with col1:

        st.caption(
            f"Stage: {runtime.stage} | Status: {runtime.status}"
        )

    with col2:

        if st.button(
            "Start Assessment",
            type="primary",
            use_container_width=True,
        ):

            try:

                engine.run(

                    st.session_state.assessment_target_type,

                    st.session_state.assessment_target,

                )

                st.success(
                    "Assessment Completed."
                )

            except Exception as e:

                runtime.emit(

                    f"ERROR: {str(e)}"

                )

                runtime.status = "Failed"

                st.error(
                    "Assessment Failed."
                )

            st.rerun()

    #
    # Runtime Console
    #
    st.markdown("### Runtime Console")

    with st.container(border=True):

        if not runtime.logs:

            st.info(
                "Runtime Ready. Click 'Start Assessment' to begin."
            )

        else:

            for event in runtime.logs:

                st.code(

                    f"[{event['time']}] {event['message']}",

                    language="text",

                )
