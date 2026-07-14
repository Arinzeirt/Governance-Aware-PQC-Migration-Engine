import streamlit as st

from controllers.navigation import render

from components.enterprise_header import show as show_header
from components.top_navigation import show as show_navigation


def show():

    show_header()

    show_navigation()

    render(
        st.session_state.page
    )

