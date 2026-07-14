from components.assessment_header import show as show_header
from components.assessment_status import show as show_status
from components.assessment_configuration import show as show_configuration

from components.runtime_dashboard import show as show_runtime_dashboard

from components.assessment_summary import show as show_summary
from components.assessment_recommendation import show as show_recommendation

from engine.runtime import runtime


def show():

    #
    # Header
    #

    show_header()

    show_status()

    #
    # Configuration
    #

    if not runtime.running and runtime.status == "Ready":

        show_configuration()

        return

    #
    # Runtime Dashboard
    #

    if runtime.running:

        show_runtime_dashboard()

        return

    #
    # Assessment Complete
    #

    if runtime.status == "Completed":

        show_summary()

        show_recommendation()

        return

    #
    # Failed
    #

    if runtime.status == "Failed":

        import streamlit as st

        st.error(

            "Assessment failed."

        )

