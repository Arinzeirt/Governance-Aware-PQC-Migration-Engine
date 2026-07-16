import streamlit as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from assessment_service import service


def show_wizard():

    st.markdown("# Enterprise PQC Migration Assessment")

    st.caption(
        "Governance-Aware Assessment • Enet Technologies"
    )

    st.divider()

    st.subheader("Assessment Target")

    st.success("Backend Services")

    with st.expander("Future Assessment Modules"):

        st.write("Database Layer")
        st.write("API Gateway")
        st.write("Cloud Infrastructure")
        st.write("Identity & Access Management")
        st.write("Kubernetes")
        st.write("Hardware Security Modules")

    st.info(
        "Analyse the selected environment and generate a governance-aware migration strategy."
    )

    st.divider()

    if st.button(
        "Begin Enterprise Assessment",
        type="primary",
        use_container_width=True,
    ):

        service.running = True

        st.session_state.screen = "progress"

        st.rerun()

