import streamlit as st

from .kpis import calculate_risk, discovery_outcome


def show():

    risk, _ = calculate_risk()

    outcome, explanation = discovery_outcome(risk)

    st.divider()

    st.markdown("### Discovery Outcome")

    st.info(
        f"""
**Outcome**

{outcome}

{explanation}
"""
    )
