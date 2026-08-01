import streamlit as st

from components.assessment_header import show as show_header
from components.assessment_status import show as show_status
from components.assessment_configuration import show as show_configuration

from components.runtime_dashboard import show as show_runtime_dashboard

from components.assessment_summary import show as show_summary
from components.assessment_recommendation import show as show_recommendation

from components.footer import show as show_footer

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

    #
    # Runtime
    #

    elif runtime.running:

        show_runtime_dashboard()

    #
    # Summary
    #

    elif runtime.status == "Completed":

        show_summary()

        st.write("")

        show_recommendation()

    #
    # Failed
    #

    elif runtime.status == "Failed":

        st.error(

            "Assessment failed."

        )

    #
    # Footer
    #

    st.write("")

    st.divider()

    show_footer()

