import streamlit as st

from design_system import (
    section_title,
)


def show_reasoning_chain(decision):

    with st.container(border=True):

        section_title(
            "Decision Reasoning",
            "Transparent governance-aware decision flow."
        )

        stages = [
            ("Discovery", "Complete"),
            ("Threat", decision["threat"]),
            ("Governance", decision["governance"]),
            ("Coverage", decision["coverage"]),
            ("Strategy", decision["strategy"]),
        ]

        cols = st.columns(len(stages))

        for col, (title, value) in zip(cols, stages):

            with col:

                st.caption(title)

                st.markdown(f"**{value}**")

        st.divider()

        st.caption(
            "Recommendation derived from inventory analysis, governance posture and migration readiness."
        )

