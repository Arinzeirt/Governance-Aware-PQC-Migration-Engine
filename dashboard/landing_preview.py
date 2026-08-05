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
# Views
#
from views.enterprise_assessment import show as enterprise_assessment
from views.research import show as research
from views.frameworks import show as frameworks
from views.about import show as about
from views.asset_detail import show as asset_detail


st.set_page_config(
    page_title="Enterprise Quantum Migration Platform (EQMP)",
    page_icon="dashboard/assets/favicon.png",
    layout="wide",
)

load()

if "page" not in st.session_state:
    st.session_state.page = "landing"

page = st.session_state.page

if page == "landing":

    navigation()

    hero()

    journey()

    enterprise_value()

    footer()

elif page == "enterprise_assessment":

    enterprise_assessment()

elif page == "research":

    navigation()

    research()

elif page == "frameworks":

    navigation()

    frameworks()

elif page == "about":

    navigation()

    about()

elif page == "asset_detail":

    navigation()

    asset_detail()

else:

    st.session_state.page = "landing"

    st.rerun()

