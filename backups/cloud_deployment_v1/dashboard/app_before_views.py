import streamlit as st

from design_system import load_design

from components.app_state import initialize_app_state
from components.launch_portal import show as show_launch_portal
from components.v1_command_center import show as show_command_center


st.set_page_config(
    page_title="EQMP Command Center",
    page_icon="dashboard/assets/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#
# Load EQMP Design System
#
load_design()

#
# Initialize Session State
#
initialize_app_state()

if "screen" not in st.session_state:
    st.session_state.screen = "launch_portal"

#
# ROUTER
#
if st.session_state.screen == "launch_portal":

    if show_launch_portal():

        st.session_state.screen = "command_center"

        st.rerun()

elif st.session_state.screen == "command_center":

    show_command_center()

else:

    st.session_state.screen = "launch_portal"

    st.rerun()

