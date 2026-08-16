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
            # Enterprise Environment
            #
            # This is the EQMP oversight boundary.
            # Discovery sources contribute evidence to this
            # environment rather than becoming the system of record.
            #
            "environment": {

                "environment_id": None,

                "organization_id": None,

                "name": "Primary Environment",

                "status": "Not Connected",

                "created_at": None,

                "last_sync": None,

                "sources": [],

                "visibility": {

                    "systems": 0,

                    "applications": 0,

                    "data_assets": 0,

                    "cryptographic_assets": 0,

                    "certificates": 0,

                },

                "discovery_gaps": 0,

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
