import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from assessment_service import service

from components.executive_header import show_executive_header
from components.executive_kpis import show_executive_kpis
from components.decision_engine import show_decision_engine
from components.reasoning_chain import show_reasoning_chain
from components.enterprise_intelligence import show_enterprise_intelligence
from components.executive_health import show_executive_health


def show_command_center():

    runtime = service.get_state()

    if not runtime["complete"]:

        st.warning("Assessment has not completed.")

        st.json(runtime)

        return

    decision = runtime["decision"]

    health = decision["health"]

    show_executive_header()

    show_executive_kpis(decision)

    st.divider()

    left, right = st.columns([1, 1])

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
