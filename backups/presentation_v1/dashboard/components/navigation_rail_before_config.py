import streamlit as st


def show():

    with st.sidebar:

        st.markdown(
            """
<div style="padding-top:10px;padding-bottom:18px;">

<div style="
font-size:34px;
font-weight:700;
color:#FFFFFF;
">

ENET

</div>

<div style="
font-size:14px;
color:#CBD5E1;
margin-top:4px;
">

Enterprise Quantum Migration Platform

</div>

</div>
""",
            unsafe_allow_html=True,
        )

        st.divider()

        st.caption("EXECUTIVE WORKSPACE")

        st.page_link("app.py", label="Dashboard")

        st.page_link("pages/assessment.py", label="Assessment")

        st.page_link("pages/inventory.py", label="Inventory")

        st.page_link("pages/reports.py", label="Reports")

        st.page_link("pages/migration.py", label="Migration Planner")

        st.divider()

        st.caption("ENGINEERING")

        st.page_link("pages/repository.py", label="Repository Explorer")

        st.page_link("pages/dashboard.py", label="Architecture")

        st.page_link("pages/dashboard.py", label="Developer Portal")

        st.divider()

        st.caption("RESEARCH")

        st.page_link("pages/research.py", label="Research Centre")

        st.page_link("pages/research.py", label="Research Notes")

        st.page_link("pages/research.py", label="Frameworks & Publications")

        st.divider()

        st.caption("ABOUT")

        st.page_link("pages/about.py", label="About EQMP")

        st.page_link("pages/about.py", label="Research Portfolio")

        st.divider()

        st.caption("Version 2.0 DEV")

        st.caption("© Enet Technologies")
