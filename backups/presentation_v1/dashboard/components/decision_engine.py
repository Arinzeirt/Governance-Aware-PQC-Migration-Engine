import streamlit as st

from components.executive_panel import executive_panel
from design_system import executive_divider


def show_decision_engine(decision):

    with executive_panel(
        "Decision Engine",
        "Governance-aware migration recommendation."
    ):

        st.markdown(
            f"## {decision['strategy']}"
        )

        confidence = int(
            decision["confidence"].replace("%", "")
        )

        st.progress(
            confidence / 100
        )

        left, right = st.columns(2)

        with left:

            st.metric(
                "Confidence",
                decision["confidence"]
            )

            st.metric(
                "Migration Mode",
                decision["mode"]
            )

        with right:

            st.metric(
                "Threat",
                decision["threat"]
            )

            st.metric(
                "Coverage",
                decision["coverage"]
            )

        executive_divider()

        st.markdown("#### Executive Action")

        st.info(
            "Begin Phase 1 migration while governance approval and compliance activities continue."
        )

