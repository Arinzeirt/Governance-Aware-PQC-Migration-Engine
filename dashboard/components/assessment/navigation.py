import streamlit as st


STEP_LABELS = {

    1: "Continue to Technology Landscape →",

    2: "Continue to Cryptographic Posture →",

    3: "Continue to Governance & Risk →",

    4: "Continue to Executive Review →",

    5: "Generate Enterprise Assessment →",

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
    # Back Button
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
    # Continue Button
    #
    with right:

        if st.button(
            STEP_LABELS.get(
                current_step,
                "Continue →",
            ),
            key="assessment_next",
            type="primary",
            use_container_width=True,
            disabled=not can_continue,
        ):

            if on_continue:

                on_continue()

            #
            # Advance to next assessment step
            #
            st.session_state.assessment["step"] += 1

            st.rerun()

    #
    # Space before footer
    #
    st.markdown(
        "<div style='height:3rem'></div>",
        unsafe_allow_html=True,
    )

