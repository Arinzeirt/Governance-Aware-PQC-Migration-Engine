import streamlit as st

from components.assessment_runner import run_assessment


def initialize_assessment():

    if "assessment_state" not in st.session_state:

        st.session_state.assessment_state = None

    if "assessment_running" not in st.session_state:

        st.session_state.assessment_running = False

    if "assessment_complete" not in st.session_state:

        st.session_state.assessment_complete = False


def start_assessment():

    initialize_assessment()

    st.session_state.assessment_running = True

    st.session_state.assessment_complete = False

    for state in run_assessment():

        st.session_state.assessment_state = state

        yield state

    st.session_state.assessment_running = False

    st.session_state.assessment_complete = True


def get_assessment_state():

    initialize_assessment()

    return st.session_state.assessment_state


def assessment_running():

    initialize_assessment()

    return st.session_state.assessment_running


def assessment_complete():

    initialize_assessment()

    return st.session_state.assessment_complete

