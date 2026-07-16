import streamlit as st


def show():

    st.divider()

    left, right = st.columns([7, 3])

    with left:

        st.caption(
            "Engineering Workspace • Research Centre"
        )

    with right:

        st.caption(
            "EQMP Technology Preview v2.0"
        )

