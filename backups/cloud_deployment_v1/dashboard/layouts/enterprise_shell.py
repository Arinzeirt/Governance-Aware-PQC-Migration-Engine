import streamlit as st


def begin():

    #
    # Reserved for future navigation shell.
    #
    pass


def end():

    st.divider()

    left, right = st.columns([8,2])

    with left:

        st.caption(
            "Developer Portal • Research Centre"
        )

    with right:

        st.caption(
            "EQMP Technology Preview v1.0"
        )
