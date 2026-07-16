import streamlit as st

from controllers.navigation import render


def show():

    #
    # Render Current Page
    #
    render(
        st.session_state.page
    )
