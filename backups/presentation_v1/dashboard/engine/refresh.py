import time

import streamlit as st

from engine.runner import runner


def refresh_if_running():

    if runner.is_running():

        time.sleep(0.5)

        st.rerun()

