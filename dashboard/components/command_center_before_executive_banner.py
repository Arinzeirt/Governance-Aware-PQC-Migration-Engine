import time

import streamlit as st

from controllers.runtime_engine import run_runtime

from components.executive_summary import show_executive_summary
from components.executive_header import show_executive_header
from components.executive_kpis import show_executive_kpis
from components.decision_engine import show_decision_engine
from components.reasoning_chain import show_reasoning_chain
from components.enterprise_intelligence import show_enterprise_intelligence
from components.executive_health import show_executive_health


def show_command_center():

    runtime = run_runtime()

    show_executive_header()

    st.divider()

    show_assessment_runtime(runtime)

    if runtime["running"]:

        time.sleep(1)

        st.rerun()

    st.divider()

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
