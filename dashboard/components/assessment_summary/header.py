import streamlit as st

from engine.runtime import runtime


def show():

    with st.container(border=True):

        left, right = st.columns([5, 1])

        with left:

            st.markdown(
                "# Enterprise Discovery Complete"
            )

            st.caption(
                "Enterprise Quantum Migration Platform (EQMP)"
            )

        with right:

            st.metric(
                "Status",
                runtime.status
            )

    st.write("")
