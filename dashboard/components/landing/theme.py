from pathlib import Path

import streamlit as st


def load():

    css = Path("dashboard/assets/theme.css")

    if css.exists():

        st.markdown(
            f"<style>{css.read_text()}</style>",
            unsafe_allow_html=True,
        )
