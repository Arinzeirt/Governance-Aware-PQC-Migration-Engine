import streamlit as st


def get_runtime():

    return st.session_state.app["assessment"]["state"]


def is_running():

    return st.session_state.app["assessment"]["running"]


def is_complete():

    return st.session_state.app["assessment"]["complete"]
