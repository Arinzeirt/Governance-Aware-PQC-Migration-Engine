import streamlit as st


def show_command_header():

    st.markdown(
        """
# Governance-Aware PQC Migration Command Center
"""
    )

    st.caption(
        "Enet Technologies • Enterprise Research Prototype • Version 3.0"
    )

    st.divider()

    left, center, right = st.columns([2, 1, 1])

    with left:

        st.success("🟢 Command Center Online")

    with center:

        st.metric(
            "Environment",
            "Research"
        )

    with right:

        st.metric(
            "Mode",
            "Assessment"
        )

