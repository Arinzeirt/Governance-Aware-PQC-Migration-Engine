import sys
from pathlib import Path

import streamlit as st

from design_system import section_title

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "app"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from analytics import get_enterprise_intelligence


def show_enterprise_intelligence():

    intelligence = get_enterprise_intelligence()

    metrics = intelligence["metrics"]

    with st.container(border=True):

        section_title(
            "Enterprise Intelligence",
            "Executive summary of assessment findings."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Assets",
                metrics["total_assets"]
            )

            st.metric(
                "High Priority",
                metrics["high_priority"]
            )

        with col2:

            st.metric(
                "Average Readiness",
                f"{metrics['average_readiness']}%"
            )

            st.metric(
                "Phase 1 Assets",
                metrics["phase1"]
            )

        st.divider()

        st.caption(
            "Detailed business, compliance and migration analytics are available in the Analytics workspace."
        )

