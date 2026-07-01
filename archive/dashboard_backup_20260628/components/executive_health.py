import streamlit as st

from design_system import section_title


def show_executive_health(health):

    with st.container(border=True):

        section_title(
            "Executive Health",
            "Current operational health of the migration programme."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Threat",
                health["threat"]
            )

            st.metric(
                "Coverage",
                health["coverage"]
            )

        with col2:

            st.metric(
                "Governance",
                health["governance"]
            )

            st.metric(
                "Readiness",
                f"{health['readiness']}%"
            )

        st.divider()

        if health["status"] == "ACTION REQUIRED":

            st.error("Action Required")

        elif health["status"] == "MONITOR":

            st.warning("Monitor")

        else:

            st.success("Healthy")

