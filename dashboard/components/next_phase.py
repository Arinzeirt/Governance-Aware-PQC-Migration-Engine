import streamlit as st


def show():

    with st.container(border=True):

        st.markdown(
            "## Recommended Next Step"
        )

        st.write(
            """
Enterprise Discovery has completed successfully.

Before EQMP can generate an enterprise migration strategy,
your organisation's business, governance and regulatory
context must now be configured.
"""
        )

        st.write("")

        if st.button(

            "Continue to Business Configuration",

            type="primary",

            use_container_width=True,

        ):

            st.session_state.page = "emcw"

            st.rerun()
