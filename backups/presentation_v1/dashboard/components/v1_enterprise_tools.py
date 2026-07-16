from pathlib import Path

import streamlit as st


def action_card(title, description):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:18px;
height:170px;
">

<div style="
font-size:20px;
font-weight:700;
color:#F8FAFC;
margin-bottom:12px;
">

{title}

</div>

<div style="
font-size:14px;
line-height:1.7;
color:#CBD5E1;
margin-bottom:18px;
">

{description}

</div>

<hr style="
border:none;
border-top:1px solid #334155;
margin:18px 0;
">

</div>
""",
        unsafe_allow_html=True,
    )


def show():

    st.markdown("## Recommended Next Steps")

    c1, c2, c3 = st.columns(3)

    with c1:

        action_card(
            "Migration Orchestrator",
            "Plan governance-approved post-quantum migration across business-critical systems."
        )

        if st.button(
            "Launch",
            key="launch_migration",
            use_container_width=True,
        ):
            st.info(
                "Migration Orchestrator will be introduced in Sprint 2."
            )

    with c2:

        action_card(
            "Executive Report",
            "Download the latest governance assessment and executive findings."
        )

        report = Path("reports/pqc_report.txt")

        if report.exists():

            with open(report, "rb") as f:

                st.download_button(
                    "Download",
                    data=f,
                    file_name="EQMP_Executive_Report.txt",
                    use_container_width=True,
                )

        else:

            st.button(
                "Download",
                disabled=True,
                use_container_width=True,
            )

    with c3:

        action_card(
            "Technical Inventory",
            "Export the discovered cryptographic inventory for engineering review."
        )

        inventory = Path("inventory.json")

        if inventory.exists():

            with open(inventory, "rb") as f:

                st.download_button(
                    "Download",
                    data=f,
                    file_name="EQMP_Inventory.json",
                    use_container_width=True,
                )

        else:

            st.button(
                "Download",
                disabled=True,
                use_container_width=True,
            )

