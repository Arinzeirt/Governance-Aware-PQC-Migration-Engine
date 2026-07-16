import streamlit as st

from controllers.navigation import render
from components.navigation_rail import show as show_navigation


def show():

    #
    # Enterprise Navigation Rail
    #
    show_navigation()

    #
    # Active Workspace
    #
    render(
        st.session_state.page
    )
