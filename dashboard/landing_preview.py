import streamlit as st

from theme.theme import load

#
# Landing Experience
#
from components.landing.navigation import show as navigation
from components.landing.hero import show as hero
from components.landing.journey import show as journey
from components.landing.enterprise_value import show as enterprise_value
from components.landing.footer import show as footer

#
# Enterprise Assessment
#
from views.enterprise_assessment import show as enterprise_assessment


st.set_page_config(
    page_title="EQMP",
    page_icon="dashboard/assets/favicon.png",
    layout="wide",
)

#
# Load Theme
#
load()

#
# Session Defaults
#
if "page" not in st.session_state:
    st.session_state.page = "landing"


#
# Router
#
if st.session_state.page == "landing":

    navigation()

    hero()

    journey()

    enterprise_value()

    footer()

elif st.session_state.page == "enterprise_assessment":

    enterprise_assessment()

else:

    st.session_state.page = "landing"

    st.rerun()

