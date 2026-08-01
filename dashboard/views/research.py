import streamlit as st

from components.asset_card import show as show_asset
from components.note_card import show as show_note
from components.publication_card import show as show_publication
from components.case_study_card import show as show_case_study
from components.roadmap import show as show_roadmap
from components.programme_status import show as show_programme

from utils.framework_registry import FRAMEWORK_REGISTRY
from utils.research_notes import load_notes


def show():

    # ==========================================================
    # Header
    # ==========================================================

    st.title("Research Centre")

    st.caption(
        "Enterprise Quantum Migration Platform • Research & Innovation"
    )

    # ==========================================================
    # Featured Research
    # ==========================================================

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:16px;
padding:32px;
margin-top:20px;
margin-bottom:28px;
">

<div style="
font-size:14px;
font-weight:700;
color:#60A5FA;
margin-bottom:10px;
">
FEATURED RESEARCH
</div>

<div style="
font-size:34px;
font-weight:700;
line-height:1.4;
color:white;
margin-bottom:18px;
">

Adaptive and Governance-Aware
Post-Quantum Cryptographic Migration
for High-Throughput Financial Systems

</div>

<div style="
font-size:16px;
line-height:1.8;
color:#CBD5E1;
">

This research investigates how governance,
enterprise architecture,
cryptographic discovery,
migration intelligence
and executive decision support
can be combined to help organisations
transition toward enterprise-wide
post-quantum cryptographic resilience.

</div>

<br>

<b>Research Status:</b> Active Research<br>
<b>Institution:</b> Manchester Metropolitan University<br>
<b>Platform:</b> Enterprise Quantum Migration Platform (EQMP)

</div>
""",
        unsafe_allow_html=True,
    )

    # ==========================================================
    # Metrics
    # ==========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Research Notes",
            "18+",
        )

    with col2:
        st.metric(
            "Frameworks",
            "5",
        )

    with col3:
        st.metric(
            "Case Studies",
            "Growing",
        )

    with col4:
        st.metric(
            "Research Status",
            "Active",
        )

    st.divider()

    # ==========================================================
    # EQMP Frameworks
    # ==========================================================

    st.subheader("EQMP Frameworks")

    frameworks = [

        (
            "Governance-Aware PQC Migration Framework",
            "A governance-driven methodology for planning and managing enterprise post-quantum migration.",
        ),

        (
            "Enterprise Quantum Readiness Framework",
            "A maturity framework for assessing organisational readiness for post-quantum cryptography.",
        ),

        (
            "Migration Decision Engine",
            "A governance-aware decision-support model for enterprise migration planning.",
        ),

        (
            "Cryptographic Discovery & Inventory Model",
            "Discovery and inventory of enterprise cryptographic assets and dependencies.",
        ),

        (
            "Compliance & Regulatory Alignment Framework",
            "Alignment of enterprise migration activities with regulatory and audit requirements.",
        ),

    ]

    cols = st.columns(2)

    for index, (title, description) in enumerate(frameworks):

        framework = FRAMEWORK_REGISTRY.get(
            title,
            {
                "type": "Framework",
                "id": "EQMP-UNK-000",
            },
        )

        with cols[index % 2]:

            show_asset(
                asset_type=framework["type"],
                asset_id=framework["id"],
                title=title,
                description=description,
                button_label="View Framework",
            )

    st.divider()

    # ==========================================================
    # EQMP Research Series
    # ==========================================================

    st.subheader("EQMP Research Series")

    notes = load_notes()

    if not notes:

        st.info("No research notes available.")

    else:

        cols = st.columns(3)

        for index, note in enumerate(notes):

            with cols[index % 3]:

               show_note(
    asset_id=note["asset_id"],
    title=note["title"],
)

    st.divider()    # ==========================================================
    # Research Outputs
    # ==========================================================

    st.subheader("Research Outputs")

    col1, col2 = st.columns(2)

    with col1:

        show_publication(
            title="Adaptive and Governance-Aware Post-Quantum Cryptographic Migration",
            venue="IEEE / ACM (Planned)",
            status="In Preparation",
            year="2027",
        )

    with col2:

        show_publication(
            title="Enterprise Cryptographic Agility for Financial Systems",
            venue="International Journal (Planned)",
            status="Planned",
            year="2028",
        )

    st.divider()

    # ==========================================================
    # Case Studies
    # ==========================================================

    st.subheader("Case Studies")

    col1, col2 = st.columns(2)

    with col1:

        show_case_study(
            title="Financial Services Migration Assessment",
            industry="Financial Services",
            status="Planned",
        )

    with col2:

        show_case_study(
            title="Government Cryptographic Readiness Assessment",
            industry="Public Sector",
            status="Planned",
        )

    st.divider()

    # ==========================================================
    # Research Roadmap
    # ==========================================================

    show_roadmap()

    st.divider()

    # ==========================================================
    # Research Programme
    # ==========================================================

    show_programme()
