import streamlit as st

from components.app_state import initialize_app_state
from components.wizard import show_wizard
from components.progress import show_progress
from components.summary import show_summary
from components.command_center import show_command_center

st.set_page_config(
    page_title="Enet PQC Migration Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_app_state()

screen = st.session_state.screen

if screen == "wizard":

    show_wizard()

elif screen == "progress":

    show_progress()

elif screen == "summary":

    show_summary()

elif screen == "command_center":

    show_command_center()

else:

    st.session_state.screen = "wizard"

    st.rerun()
