import streamlit as st

from components.ui.section_header import show as header
from content.registration import FIELDS


def show():

    header(
        "Start Basic Assessment",
        "Register your organisation to receive an executive assessment report.",
    )

    values = {}

    for field in FIELDS:

        values[field["key"]] = st.text_input(
            field["label"],
            key=field["key"],
        )

    st.write("")

    if st.button(
        "Continue to Assessment",
        key="registration_continue",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.registration = values

        st.session_state.page = "basic_assessment"

        st.rerun()
