import streamlit as st


def show(
    current_step,
    can_continue=True,
    on_continue=None,
):

    left, right = st.columns([1, 1])

    with left:

        if current_step > 1:

            if st.button(
                "← Back",
                key="assessment_back",
            ):

                st.session_state.assessment["step"] -= 1
                st.rerun()

    with right:

        label = (
            "Start Quantum Readiness Assessment"
            if current_step == 4
            else "Continue →"
        )

        if st.button(
            label,
            key="assessment_next",
            type="primary",
            use_container_width=True,
            disabled=not can_continue,
        ):

            if on_continue:

                on_continue()

            if current_step < 4:

                st.session_state.assessment["step"] += 1

            st.rerun()
