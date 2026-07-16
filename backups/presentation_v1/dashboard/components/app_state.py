import streamlit as st


def initialize_app_state():

    if "screen" not in st.session_state:

        st.session_state.screen = "launch_portal"

    if "app" not in st.session_state:

        st.session_state.app = {

            "presentation_mode": True,

            "assessment": {

                "running": False,

                "complete": False,

                "started": False,

                "ui_loaded": False,

                "state": None,

            }

        }
