import streamlit as st

from engine.runtime import runtime
from engine.session import session


def show():

    st.divider()

    st.markdown("### Discovery Metadata")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Repository",
            runtime.repository_name or "-"
        )

    with m2:
        st.metric(
            "Files Scanned",
            runtime.total_files
        )

    with m3:
        st.metric(
            "Session",
            session.session_id
        )

    st.divider()

    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric(
            "Assets Identified",
            runtime.findings
        )

    with s2:
        st.metric(
            "High Risk",
            runtime.critical
        )

    with s3:
        st.metric(
            "Medium Risk",
            runtime.medium
        )
