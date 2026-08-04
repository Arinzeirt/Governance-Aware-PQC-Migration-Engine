import streamlit as st

from components.assessment.shell import show as shell
from components.assessment.overview import show as overview


def placeholder(title):

    def render():

        st.markdown(f"## {title}")

        st.info("This section will be implemented in the next phase.")

    return render


def show():

    if "assessment" not in st.session_state:

        st.session_state.assessment = {

            "step": 1,

            "overview": {},

            "technology": {},

            "cryptography": {},

            "configuration": {},

        }

    step = st.session_state.assessment["step"]

    page_configs = {

        1: {
            "renderer": overview,
            "can_continue": False,
            "on_continue": None,
        },

        2: {
            "renderer": placeholder("Technology Landscape"),
        },

        3: {
            "renderer": placeholder("Cryptography Overview"),
        },

        4: {
            "renderer": placeholder("Assessment Configuration"),
        },

    }

    config = page_configs[step]

    shell(
        {
            "step": step,
            "renderer": config["renderer"],
            "can_continue": config.get("can_continue", True),
            "on_continue": config.get("on_continue"),
        }
    )
