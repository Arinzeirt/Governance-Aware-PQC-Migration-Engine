from pathlib import Path

import streamlit as st

from engine.runtime import runtime
from engine.session import session
from engine.runner import runner


def show():

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "Continue to Migration",
            type="primary",
            width="stretch",
        ):

            st.session_state.page = "repository"

            st.rerun()

    with c2:

        report = Path(
            "reports/pqc_executive_report.pdf"
        )

        if report.exists():

            with open(report, "rb") as f:

                st.download_button(

                    "Export Executive Report",

                    data=f,

                    file_name="EQMP_Executive_Report.pdf",

                    mime="application/pdf",

                    width="stretch",

                )

        else:

            st.button(

                "Export Executive Report",

                disabled=True,

                width="stretch",

            )

    with c3:

        inventory = Path(
            "inventory.json"
        )

        if inventory.exists():

            with open(inventory, "rb") as f:

                st.download_button(

                    "Download Inventory",

                    data=f,

                    file_name="inventory.json",

                    mime="application/json",

                    width="stretch",

                )

        else:

            st.button(

                "Download Inventory",

                disabled=True,

                width="stretch",

            )

    st.divider()

    st.caption(
        "Enterprise Discovery is the first phase of the governance-aware post-quantum migration lifecycle. Continue to the Migration workspace to review readiness, inventory, and migration priorities."
    )

    st.write("")

    if st.button(
        "Start New Discovery",
        width="stretch",
    ):

        runtime.new_assessment()

        session.reset()

        runner.running = False

        st.rerun()
