import streamlit as st


def show_executive_summary(runtime):

    st.success("✅ Enterprise Assessment Completed")

    st.markdown("## Executive Overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Overall Risk",
            "HIGH"
        )

    with c2:
        st.metric(
            "Readiness",
            "18%"
        )

    with c3:
        st.metric(
            "Assets",
            "573"
        )

    with c4:
        st.metric(
            "Compliance",
            "ACTION REQUIRED"
        )

    with c5:
        st.metric(
            "Confidence",
            "92%"
        )

    st.info(
        """
The assessment indicates significant use of traditional
public-key cryptography across business-critical systems.

A governance-led phased migration strategy is recommended
to improve post-quantum readiness while maintaining
business continuity.
"""
    )
