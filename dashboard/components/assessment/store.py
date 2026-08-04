import streamlit as st
from datetime import datetime


def save(section, data):

    if "assessment" not in st.session_state:

        st.session_state.assessment = {}

    st.session_state.assessment[section] = data

    st.session_state.assessment_last_saved = datetime.now()


def load(section):

    if "assessment" not in st.session_state:

        return {}

    return st.session_state.assessment.get(section, {})


def last_saved():

    return st.session_state.get(
        "assessment_last_saved",
        None,
    )


def assessment_id():

    return st.session_state.get(
        "assessment_id",
        None,
    )


def set_assessment_id(value):

    if "assessment_id" not in st.session_state:

        st.session_state.assessment_id = value
