import streamlit as st


def show():

    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True,
    )

    left, centre, right = st.columns([2, 3, 2])

    with centre:

        if st.button(
            "Start Enterprise Assessment →",
            type="primary",
            use_container_width=True,
            key="hero_cta",
        ):

            #
            # Launch Enterprise Assessment
            #
            st.session_state.page = "enterprise_assessment"

            st.rerun()

    st.markdown(
        "<div style='height:24px'></div>",
        unsafe_allow_html=True,
    )

    st.divider()

