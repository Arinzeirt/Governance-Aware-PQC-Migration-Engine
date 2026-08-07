import streamlit as st

from utils.ui import scroll_to_top

from components.assessment.header import show as header
from components.assessment.progress import show as progress
from components.assessment.navigation import show as navigation

from components.landing.footer import show as footer


def show(content):

    #
    # Always start new assessment pages
    # from the top.
    #
    scroll_to_top()

    step = content["step"]

    #
    # Assessment Header
    #
    header()

    #
    # Assessment Journey
    #
    progress(step)

    #
    # Current Assessment Page
    #
    result = content["renderer"]()

    #
    # Space before navigation
    #
    st.markdown(
        "<div style='height:2rem'></div>",
        unsafe_allow_html=True,
    )

    #
    # Navigation
    #
    navigation(
        step,
        can_continue=result.get(
            "can_continue",
            True,
        ),
        on_continue=result.get(
            "on_continue",
        ),
    )

    #
    # Space before footer
    #
    st.markdown(
        "<div style='height:4rem'></div>",
        unsafe_allow_html=True,
    )

    #
    # Shared Footer
    #
    footer()

