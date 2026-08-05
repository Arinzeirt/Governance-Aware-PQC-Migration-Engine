from pathlib import Path

import streamlit as st

from components.note_card import show as show_note
from components.landing.footer import show as show_footer

from utils.research_notes import load_notes


def show():

    selected = st.session_state.get("selected_note")

    if not selected:

        st.warning("No research note selected.")

        if st.button("← Back to Research Centre"):

            st.session_state.page = "research"
            st.rerun()

        return

    note = Path(selected)

    if not note.exists():

        st.error("Research note not found.")

        if st.button("← Back to Research Centre"):

            st.session_state.page = "research"
            st.rerun()

        return

    #
    # Header
    #

    if st.button(
        "← Back to Research Centre",
        use_container_width=False,
    ):

        st.session_state.page = "research"

        st.rerun()

    st.title("Research Centre")

    st.caption(
        "Research Notes Series"
    )

    st.divider()

    #
    # Research Note
    #

    st.markdown(
        note.read_text(
            encoding="utf-8"
        )
    )

    st.divider()

    #
    # Continue Reading
    #

    st.subheader("Continue Reading")

    st.caption(
        "Explore additional research notes related to enterprise quantum readiness, governance and post-quantum migration."
    )

    notes = load_notes()

    current = note.resolve()

    related = [

        n for n in notes

        if n["path"].resolve() != current

    ]

    cols = st.columns(3)

    for index, item in enumerate(related[:3]):

        with cols[index]:

            show_note(
                asset_id=item["asset_id"],
                title=item["title"],
            )

    st.divider()

    show_footer()

