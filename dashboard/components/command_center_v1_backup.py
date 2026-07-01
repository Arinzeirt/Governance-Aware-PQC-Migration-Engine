import streamlit as st

from controllers.demo_runtime import run_runtime

from components.executive_summary import show_executive_summary
from components.executive_header import show_executive_header
from components.executive_kpis import show_executive_kpis
from components.decision_engine import show_decision_engine
from components.reasoning_chain import show_reasoning_chain
from components.enterprise_intelligence import show_enterprise_intelligence
from components.executive_health import show_executive_health


def show_command_center():

    assessment = st.session_state.app["assessment"]

    #
    # FIRST VISIT
    # Render dashboard immediately.
    #
    if not assessment["ui_loaded"]:

        assessment["ui_loaded"] = True

        show_executive_header()

        st.divider()

        st.info("Preparing Executive Assessment...")

        st.progress(0)

        st.caption(
            "Initializing Governance-Aware PQC Assessment..."
        )

        st.rerun()

        return

    #
    # Start assessment after dashboard is already visible.
    #
    runtime = run_runtime()

    show_executive_header()

    st.divider()

    show_executive_summary(runtime)

    #
    # Assessment still running
    #
    if runtime["running"]:

        st.info(
            "Generating Executive Intelligence..."
        )

        st.rerun()

        return

    #
    # Assessment Complete
    #
    decision = runtime["decision"]

    health = decision["health"]

    st.divider()

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
