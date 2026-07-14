"""
Enet Design System

CSS Loader
"""

from pathlib import Path
import streamlit as st


def load():
    """
    Load the Enet Design System CSS.
    """

    css_file = Path("dashboard/assets/shell.css")

    if css_file.exists():

        st.markdown(
            f"<style>{css_file.read_text()}</style>",
            unsafe_allow_html=True,
        )

