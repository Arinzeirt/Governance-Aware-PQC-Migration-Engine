from pathlib import Path

import streamlit as st


def action_card(
    title,
    description,
    button_text,
    key,
    download=None,
    callback=None,
):

    st.markdown(
        f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:20px;
height:180px;
">

<div style="
font-size:20px;
font-weight:700;
color:#F8FAFC;
margin-bottom:14px;
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
margin:16px 0;
">
</div>
""",
        unsafe_allow_html=True,
    )

    if download:

        path, filename = download

        if path.exists():

            with open(path, "rb") as f:

                st.download_button(
                    button_text,
                    data=f,
                    file_name=filename,
                    mime="application/pdf" if filename.endswith(".pdf") else "text/plain",
                    key=key,
                    use_container_width=True,
                )

        else:

            st.button(
                button_text,
                disabled=True,
                key=key,
                use_container_width=True,
            )

    else:

        if st.button(
            button_text,
            key=key,
            use_container_width=True,
        ):

            if callback:
                callback()


def show():

    st.markdown("## Recommended Next Steps")

    c1, c2, c3 = st.columns(3)

    with c1:

        action_card(
            "Migration Orchestrator",
            "Plan governance-led post-quantum migration across business-critical systems.",
            "Launch",
            "migration",
            callback=lambda: st.toast(
                "Migration Orchestrator arrives in Sprint 2."
            ),
        )

    with c2:

        action_card(
            "Executive Report",
            "Download the latest executive governance assessment.",
            "Download",
            "report",
            download=(
                Path("reports/pqc_executive_report.pdf"),
                "EQMP_Executive_Report.pdf",
            ),
        )

    with c3:

        action_card(
            "Technical Inventory",
            "Export the discovered cryptographic inventory for engineering review.",
            "Download",
            "inventory",
            download=(
                Path("inventory.json"),
                "EQMP_Inventory.json",
            ),
        )
