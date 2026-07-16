import streamlit as st


def show():

    with st.container(border=True):

        left, right = st.columns([5,1])

        with left:

            st.markdown("## Executive Summary")

            st.caption(
                "Governance-Aware Post-Quantum Readiness"
            )

            st.write(
                "Your enterprise has identified cryptographic assets requiring governance-led migration planning before the quantum threat becomes operational."
            )

            st.markdown(
                "**Executive Decision**"
            )

            st.info(
                "Begin a governance-led migration programme prioritizing Internet-facing and business-critical systems."
            )

        with right:

            st.success(
                "Assessment\nCompleted"
            )
