import streamlit as st

from design_system import load_design

from components.app_state import initialize_app_state
from components.launch_portal import show as show_launch_portal

from layouts.shell import show as show_shell


st.set_page_config(
    page_title="EQMP Command Center",
    page_icon="dashboard/assets/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#
# Load Design System
#
load_design()

#
# Initialize Session
#
initialize_app_state()

#
# Application State
#
if "screen" not in st.session_state:
    st.session_state.screen = "launch_portal"

#
# Navigation State
#
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

#
# Application Router
#
if st.session_state.screen == "launch_portal":

    if show_launch_portal():

        st.session_state.screen = "command_center"

        st.rerun()

elif st.session_state.screen == "command_center":

    show_shell()

else:

    st.session_state.screen = "launch_portal"

    st.rerun()
