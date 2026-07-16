from pathlib import Path
import streamlit as st


def load_design():

    css = Path("dashboard/assets/dashboard.css")

    if css.exists():

        st.markdown(

            f"<style>{css.read_text()}</style>",

            unsafe_allow_html=True,

        )
