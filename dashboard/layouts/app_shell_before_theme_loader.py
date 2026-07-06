import streamlit as st

from layouts.header import show as show_header
from layouts.drawer import show as show_drawer
from layouts.workspace import show as show_workspace
from layouts.footer import show as show_footer


def show():

    #
    # Enterprise Header
    #
    show_header()

    #
    # Navigation Drawer
    #
    show_drawer()

    #
    # Current Workspace
    #
    show_workspace()

    #
    # Footer
    #
    show_footer()

