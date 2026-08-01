import streamlit as st

from controllers.navigation import render

from components.enterprise_header import show as show_header
from components.top_navigation import show as show_navigation

from layouts.asset_workspace import show as show_asset_workspace


def show():

    page = st.session_state.page

    #
    # Knowledge Assets
    #
    if page == "asset_detail":
        show_asset_workspace()
        return

    #
    # Application Workspace
    #
    show_header()

    show_navigation()

    render(page)
