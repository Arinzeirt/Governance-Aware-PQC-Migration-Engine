import streamlit as st

from components.executive_header import show_executive_header
from components.executive_summary import show_executive_summary


def show_command_center():

    show_executive_header()

    st.divider()

    show_executive_summary({})

    st.divider()

    st.subheader("Executive KPI Cards")
    st.info("Coming next...")

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Enterprise Scan Results")
        st.info("Coming next...")

    with right:

        st.subheader("Environment Summary")
        st.info("Coming next...")

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Compliance Readiness")
        st.info("Coming next...")

    with right:

        st.subheader("Executive Decision")
        st.info("Coming next...")

    st.divider()

    st.subheader("Top Findings")
    st.info("Coming next...")

    st.divider()

    st.subheader("Executive Advisory")
    st.info("Coming next...")

    st.divider()

    st.subheader("Executive Roadmap")
    st.info("Coming next...")
