import streamlit as st


STEP_LABELS = {
    1: "Continue to Technology Landscape →",
    2: "Continue to Cryptography Overview →",
    3: "Continue to Assessment Configuration →",
    4: "Generate Quantum Readiness Assessment →",
}


def show(
    current_step,
    can_continue=True,
    on_continue=None,
):

    #
    # Space above navigation
    #
    st.markdown(
        "<div style='height:2rem'></div>",
        unsafe_allow_html=True,
    )

    #
    # Navigation Layout
    #
    left, spacer, right = st.columns([3, 3, 4])

    #
    # Back
    #
    with left:

        if current_step > 1:

            if st.button(
                "← Back",
                key="assessment_back",
                use_container_width=True,
            ):

                st.session_state.assessment["step"] -= 1
                st.rerun()

    #
    # Spacer
    #
    with spacer:
        st.empty()

    #
    # Continue
    #
    with right:

        if st.button(
            STEP_LABELS[current_step],
            key="assessment_next",
            type="primary",
            use_container_width=True,
            disabled=not can_continue,
        ):

            if on_continue:
                on_continue()

            #
            # TEMPORARY
            # Technology Landscape is not yet implemented.
            #
            if current_step == 1:

                st.info(
                    "Technology Landscape is currently under development. This concludes the current assessment preview."
                )

            else:

                if current_step < 4:
                    st.session_state.assessment["step"] += 1

                st.rerun()

    #
    # Space before footer
    #
    st.markdown(
        "<div style='height:3rem'></div>",
        unsafe_allow_html=True,
    )

