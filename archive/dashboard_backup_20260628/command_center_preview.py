import streamlit as st
from theme import load_theme

from components.app_state import initialize_app_state
from components.command_center import show_command_center

st.set_page_config(
    page_title="Command Center Preview",
    layout="wide"
)
load_theme()

initialize_app_state()

if st.session_state.app["assessment"]["state"] is None:

    st.session_state.app["assessment"]["state"] = {

        "session": "PQC-DEMO-001",

        "progress": 65,

        "current": "Cryptographic Discovery",

        "operation": "Scanning backend services..."

    }

show_command_center()
