import streamlit as st


def initialize_app_state():

    if "screen" not in st.session_state:

        st.session_state.screen = "launch_portal"

    if "app" not in st.session_state:

        st.session_state.app = {

            "assessment": {

                "running": False,

                "complete": False,

                "state": None,

            }

        }
