import streamlit as st


def show():

    if st.button(
        "Start Enterprise Assessment →",
        type="primary",
        use_container_width=True,
    ):

        # =====================================================
        # Start a completely fresh assessment
        # =====================================================

        st.session_state["assessment"] = {
            "step": 1,
        }

        # The previous assessment may have reached
        # the executive results layer. Clear that route state.
        st.session_state["assessment_results"] = False

        # Clear any temporary preview/result routing state.
        st.session_state.pop(
            "preview",
            None,
        )

        # Route into the assessment.
        st.session_state.page = "enterprise_assessment"

        st.rerun()
