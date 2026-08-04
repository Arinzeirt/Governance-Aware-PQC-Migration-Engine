import streamlit as st

from .form import show as organisation_form

from components.assessment.summary_panel import show as summary_panel

from components.assessment.research_brief import (
    show as research_brief,
)

from components.assessment.research_brief.briefs import (
    OVERVIEW,
)


def show():

    #
    # Top Layout
    #

    left, right = st.columns(
        [7, 3],
        gap="large",
    )

    with left:

        result = organisation_form()

    with right:

        summary_panel(
            current_step="Overview",
            completed=result["completed"],
            total=result["total"],
        )

    #
    # Research Brief
    #

    left, right = st.columns(
        [7, 3],
        gap="large",
    )

    with left:

        research_brief(
            OVERVIEW,
        )

    with right:

        #
        # Keep sidebar alignment.
        #
        st.empty()

    return {

        "can_continue":
            result["can_continue"],

        "on_continue":
            result["on_continue"],

    }
