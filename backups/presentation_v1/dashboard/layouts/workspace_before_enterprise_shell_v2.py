import streamlit as st

from controllers.navigation import render
from components.navigation_menu import show as show_menu


def show():

    navigation, workspace = st.columns(
        [1, 4],
        gap="large"
    )

    with navigation:

        show_menu()

    with workspace:

        render(
            st.session_state.page
        )

