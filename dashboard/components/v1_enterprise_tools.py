from pathlib import Path

import streamlit as st


def show():

    with st.expander("▸ Enterprise Tools", expanded=False):

        if st.button(
            "Launch Migration Planner",
            use_container_width=True,
        ):
            st.info(
                "This feature is available in the Enterprise Edition."
            )

        report = Path("reports/pqc_report.txt")

        if report.exists():

            with open(report, "rb") as f:

                st.download_button(
                    "Download Executive Report",
                    data=f,
                    file_name="EQMP_Executive_Report.txt",
                    use_container_width=True,
                )

        else:

            st.button(
                "Download Executive Report",
                disabled=True,
                use_container_width=True,
            )

        inventory = Path("inventory.json")

        if inventory.exists():

            with open(inventory, "rb") as f:

                st.download_button(
                    "Download Technical Inventory",
                    data=f,
                    file_name="EQMP_Inventory.json",
                    use_container_width=True,
                )

        else:

            st.button(
                "Download Technical Inventory",
                disabled=True,
                use_container_width=True,
            )

