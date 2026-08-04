import streamlit as st

from theme.theme import load
from pages.assessment import show


st.set_page_config(
    page_title="EQMP Assessment",
    layout="wide",
)

load()

show()
