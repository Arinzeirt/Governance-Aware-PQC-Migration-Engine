import streamlit as st

from controllers.runtime_engine import update_runtime

from components.assessment_runtime_panel import show_assessment_runtime
from components.executive_header import show_executive_header
from components.executive_kpis import show_executive_kpis
from components.decision_engine import show_decision_engine
from components.reasoning_chain import show_reasoning_chain
from components.enterprise_intelligence import show_enterprise_intelligence
from components.executive_health import show_executive_health


def show_command_center():

    runtime = update_runtime()

    show_executive_header()

    st.divider()

    show_assessment_runtime(runtime)

    st.divider()

    if not runtime["complete"]:

        st.info("Assessment is running...")

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

    left, right = st.columns([2, 1])

    with left:
        show_enterprise_intelligence()

    with right:
        show_executive_health(health)
