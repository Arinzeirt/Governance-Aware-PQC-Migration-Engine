import streamlit as st

from design_system import load_design
from components.app_state import initialize_app_state
from layouts.app_shell import show as show_shell


st.set_page_config(
    page_title="EQMP Enterprise Shell",
    page_icon="dashboard/assets/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_design()

initialize_app_state()

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

show_shell()

