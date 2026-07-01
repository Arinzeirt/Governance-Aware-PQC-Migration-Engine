import streamlit as st

from components.assessment_runner import run_assessment
from components.assessment_runtime_panel import show_assessment_runtime

from components.executive_header import show_executive_header
from components.executive_kpis import show_executive_kpis
from components.decision_engine import show_decision_engine
from components.reasoning_chain import show_reasoning_chain
from components.enterprise_intelligence import show_enterprise_intelligence
from components.executive_health import show_executive_health


def show_command_center():

    assessment = st.session_state.app["assessment"]

    # First visit: automatically start the assessment
    if assessment["state"] is None:

        for runtime in run_assessment():

            show_executive_header()

            st.divider()

            show_assessment_runtime(runtime)

            st.rerun()

        return

    runtime = assessment["state"]

    show_executive_header()

    st.divider()

    show_assessment_runtime(runtime)

    st.divider()

    if not assessment["complete"]:

        st.info(
            "Assessment is still running..."
        )

        st.rerun()

        return

    decision = runtime["decision"]

    health = decision["health"]

    show_executive_kpis(decision)

    st.divider()

    left, right = st.columns(2)

    with left:

        show_decision_engine(decision)

    with right:

        show_reasoning_chain(decision)

    st.divider()

    left, right = st.columns([2,1])

    with left:

        show_enterprise_intelligence()

    with right:

        show_executive_health(health)
