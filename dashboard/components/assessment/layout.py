import streamlit as st

from components.assessment.summary_panel import show as summary_panel
from components.assessment.research_brief import show as research_brief


def show(
    *,
    current_step,
    form,
    research,
):
    """
    Standard assessment page layout.

    Every assessment page should use this layout.

    Layout

    ┌─────────────────────────────┬────────────────────┐
    │ Form                        │ Assessment Summary │
    │                             │                    │
    │ Research Brief              │                    │
    └─────────────────────────────┴────────────────────┘
    """

    main, sidebar = st.columns(
        [7, 3],
        gap="large",
    )

    #
    # Main Content
    #
    with main:

        result = form()

        research_brief(
            research,
        )

    #
    # Sidebar
    #
    with sidebar:

        summary_panel(
            current_step=current_step,
            completed=result["completed"],
            total=result["total"],
        )

    return result
