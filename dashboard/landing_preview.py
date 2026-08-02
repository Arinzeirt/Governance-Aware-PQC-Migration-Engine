import streamlit as st

from theme.theme import load

from components.landing.navigation import show as navigation
from components.landing.hero import show as hero
from components.landing.journey import show as journey
from components.landing.enterprise_value import show as enterprise_value
from components.landing.footer import show as footer

st.set_page_config(
    page_title="EQMP Landing Preview",
    layout="wide",
)

load()
#
# Load Enterprise Theme
#
load()

#
# Landing Page
#

navigation()

hero()

journey()

enterprise_value()
footer()
