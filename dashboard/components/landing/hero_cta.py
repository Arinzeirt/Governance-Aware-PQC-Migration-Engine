import streamlit as st


def show():

    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True,
    )

    left, centre, right = st.columns([2,3,2])

    with centre:

        if st.button(
            "Start Basic Assessment →",
            type="primary",
            use_container_width=True,
            key="hero_cta",
        ):

            st.session_state.page = "registration"

            st.rerun()

    st.markdown(
        "<div style='height:24px'></div>",
        unsafe_allow_html=True,
    )

    st.divider()
