import streamlit as st
from pathlib import Path


def show_quick_actions():

    st.subheader("Quick Actions")

    c1, c2, c3 = st.columns(3)

    #
    # Executive Report
    #

    with c1:

        report = Path("reports/pqc_report.txt")

        if report.exists():

            with open(report, "rb") as f:

                st.download_button(

                    "⬇ Executive Report",

                    data=f,

                    file_name="EQMP_Executive_Report.txt",

                    use_container_width=True,

                )

        else:

            st.button(

                "⬇ Executive Report",

                disabled=True,

                use_container_width=True,

            )

    #
    # Inventory
    #

    with c2:

        inventory = Path("inventory.json")

        if inventory.exists():

            with open(inventory, "rb") as f:

                st.download_button(

                    "⬇ Inventory",

                    data=f,

                    file_name="EQMP_Inventory.json",

                    use_container_width=True,

                )

        else:

            st.button(

                "⬇ Inventory",

                disabled=True,

                use_container_width=True,

            )

    #
    # Refresh
    #

    with c3:

        if st.button(

            "🔄 Refresh Assessment",

            use_container_width=True,

        ):

            st.rerun()
