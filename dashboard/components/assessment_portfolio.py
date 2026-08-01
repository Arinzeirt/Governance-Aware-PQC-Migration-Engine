import streamlit as st


def show():

    st.title("Assessment Portfolio")

    st.caption(
        "Manage enterprise cryptographic assessment projects."
    )

    st.divider()

    if st.button(
        "New Assessment",
        type="primary",
        use_container_width=True,
    ):

        st.info(
            "Assessment creation wizard coming in RC2.5."
        )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "No assessment projects yet."
        )

        st.caption(
            "Start a new enterprise assessment to begin."
        )
