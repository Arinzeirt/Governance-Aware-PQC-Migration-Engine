import streamlit as st

from layout.sidebar import show as show_sidebar
from layout.workspace import show as show_workspace


def show():

    #
    # Two-column enterprise layout
    #
    nav, workspace = st.columns(
        [1.2, 5],
        gap="medium",
    )

    #
    # Left Navigation
    #
    with nav:
        show_sidebar()

    #
    # Main Workspace
    #
    with workspace:
        show_workspace()

