import streamlit as st

from content.assessment import STEPS

from components.assessment.summary_panel import show as summary_panel


def show(
    *,
    current_step,
    form,
):

    #
    # Resolve display information from the
    # internal numeric step.
    #

    step = next(
        (
            item
            for item in STEPS
            if item["id"] == current_step
        ),
        STEPS[0],
    )

    main, sidebar = st.columns(
        [7.5, 2.5],
        gap="large",
    )

    with main:

        result = form()

    with sidebar:

        summary_panel(
            current_step=current_step,
            current_step_label=step["title"],
            completed=result["completed"],
            total=result["total"],
            can_continue=result.get(
                "can_continue",
                False,
            ),
            on_continue=result.get(
                "on_continue",
            ),
        )

    return result
