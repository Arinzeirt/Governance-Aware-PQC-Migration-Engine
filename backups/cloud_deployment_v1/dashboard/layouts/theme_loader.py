from pathlib import Path
import streamlit as st


def load_shell():

    css = Path(
        "dashboard/assets/shell.css"
    ).read_text()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )

