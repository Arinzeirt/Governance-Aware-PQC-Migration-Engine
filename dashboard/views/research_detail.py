from pathlib import Path

import streamlit as st


def show():

    st.title("Research Note")

    selected = st.session_state.get("selected_note")

    if not selected:

        st.warning("No research note selected.")

        if st.button("← Back to Research Centre"):

            st.session_state["page"] = "research"
            st.rerun()

        return

    note = Path(selected)

    if not note.exists():

        st.error("Research note not found.")

        if st.button("← Back"):

            st.session_state["page"] = "research"
            st.rerun()

        return

    if st.button("← Back to Research Centre"):

        st.session_state["page"] = "research"
        st.rerun()

    st.divider()

    st.markdown(note.read_text(encoding="utf-8"))
