import streamlit as st


def initialize_app_state():
    """
    Initialize the global EQMP application state.

    This creates a single application container that every module can
    share instead of maintaining independent session variables.
    """

    #
    # Global screen routing
    #
    if "screen" not in st.session_state:
        st.session_state.screen = "launch_portal"

    #
    # Global application state
    #
    if "app" not in st.session_state:

        st.session_state.app = {

            #
            # UI Mode
            #
            "presentation_mode": True,

            #
            # Assessment Runtime
            #
            "assessment": {

                "running": False,

                "complete": False,

                "started": False,

                "ui_loaded": False,

                #
                # Runtime object produced by assessment_runner.py
                #
                "state": None,

            },

            #
            # Executive Dashboard
            #
            "dashboard": {

                "loaded": False,

                "last_refresh": None,

            },

            #
            # Migration Workspace
            # (formerly Repository)
            #
            "migration": {

                "loaded": False,

                "active_view": "overview",

                "filters": {},

            },

            #
            # Inventory
            #
            "inventory": {

                "loaded": False,

                "last_sync": None,

            },

            #
            # Reports
            #
            "reports": {

                "loaded": False,

                "last_generated": None,

                "available": [],

            },

            #
            # Research Centre
            #
            "research": {

                "loaded": False,

                "active_section": "overview",

                "filters": {},

            },

            #
            # Navigation
            #
            "navigation": {

                "selected_page": "dashboard",

                "history": [],

            }

        }
