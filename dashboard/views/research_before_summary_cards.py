import streamlit as st

from utils.research_notes import load_notes

from components.research_card import show as show_card


def show():

    st.title("Research Centre")

    st.caption(
        "Enterprise Quantum Migration Platform • Research & Innovation"
    )

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:28px;
margin-top:20px;
margin-bottom:30px;
">

<div style="
font-size:14px;
color:#60A5FA;
font-weight:600;
margin-bottom:8px;
">

FEATURED RESEARCH

</div>

<div style="
font-size:30px;
font-weight:700;
color:white;
margin-bottom:15px;
">

Adaptive and Governance-Aware Post-Quantum Cryptographic Migration
for High-Throughput Financial Systems

</div>

<div style="
color:#CBD5E1;
font-size:16px;
line-height:1.7;
">

This research investigates how governance, enterprise architecture,
cryptographic discovery and migration intelligence can be combined
to help organisations transition from classical cryptography to
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

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Research Notes",
            "18+"
        )

    with col2:
        st.metric(
            "Frameworks",
            "4"
        )

    with col3:
        st.metric(
            "Case Studies",
            "Growing"
        )

    with col4:
        st.metric(
            "Research Status",
            "Active"
        )

    st.divider()

    st.subheader("Research Overview")

    st.write(
        """
The Enterprise Quantum Migration Platform (EQMP) is supported by an
ongoing programme of research focused on governance-aware
post-quantum cryptographic migration.

The objective is to help organizations transition toward
quantum-resistant cryptography using structured governance,
enterprise architecture, migration planning and executive
decision support.
"""
    )

    st.divider()

    st.subheader("Research Portfolio")

    frameworks = [

        (
            "Governance-Aware PQC Migration Framework",
            "A governance-driven methodology for planning and managing enterprise post-quantum migration."
        ),

        (
            "Enterprise Quantum Readiness Framework",
            "A maturity framework for assessing organisational readiness for post-quantum cryptography."
        ),

        (
            "Migration Decision Engine",
            "A decision-support model that prioritises migration activities based on governance, business impact and cryptographic risk."
        ),

        (
            "Cryptographic Discovery & Inventory Model",
            "An enterprise discovery model for identifying cryptographic assets and establishing migration inventories."
        ),

        (
            "Compliance & Regulatory Alignment Framework",
            "A governance framework that aligns post-quantum migration activities with regulatory, compliance and audit requirements."
        ),

        (
            "AI-Assisted Migration Intelligence Framework (Coming Soon)",
            "Future research exploring AI-assisted migration planning, prioritisation and executive decision support."
        ),

        (
            "Enterprise Cryptographic Agility Framework (Coming Soon)",
            "Future research focused on enterprise-wide cryptographic agility, lifecycle management and long-term resilience."
        ),

    ]

    cols = st.columns(2)

    for index, (title, description) in enumerate(frameworks):

        with cols[index % 2]:

            show_card(
                title=title,
                description=description,
                item_id=f"framework_{index}",
                button_label=(
                    "Coming Soon"
                    if "Coming Soon" in title
                    else "View Framework"
                ),
            )

    st.divider()

    st.subheader("Research Notes")

    notes = load_notes()

    if not notes:
        st.info("No research notes available.")
    else:
        for note in notes:

            st.markdown(
                f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:12px;
padding:18px;
margin-bottom:14px;
">

<div style="
font-size:18px;
font-weight:700;
color:white;
margin-bottom:8px;
">

Research Note {note['id']}

</div>

<div style="
font-size:14px;
color:#CBD5E1;
margin-bottom:12px;
">

{note['title']}

</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.divider()

    st.subheader("Publications & Knowledge Library")

    publications = [

        (
            "Journal Publications",
            "Peer-reviewed research in post-quantum cryptography, enterprise security and governance."
        ),

        (
            "Conference Papers",
            "Conference presentations and technical publications supporting EQMP research."
        ),

        (
            "White Papers",
            "Enterprise guidance on governance-aware migration and cryptographic agility."
        ),

        (
            "Technical Reports",
            "Implementation guidance, migration assessments and engineering documentation."
        ),

    ]

    cols = st.columns(2)

    for index, (title, description) in enumerate(publications):

        with cols[index % 2]:

            st.markdown(
                f"""
<div style="
background:#111827;
border:1px solid #334155;
border-radius:14px;
padding:20px;
margin-bottom:18px;
min-height:170px;
">

<div style="
font-size:20px;
font-weight:700;
color:white;
margin-bottom:12px;
">

{title}

</div>

<div style="
color:#CBD5E1;
line-height:1.6;
font-size:14px;
">

{description}

</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.divider()

    st.subheader("Case Studies")

    st.info("Financial Services")

    st.info("Government")

    st.info("Critical Infrastructure")

    st.info("Enterprise Migration")

    st.divider()

    st.subheader("Research Roadmap")

    roadmap = [
        "Governance-Aware Migration",
        "Enterprise Decision Engine",
        "AI-assisted Migration Planning",
        "Automated Cryptographic Discovery",
        "Enterprise Quantum Readiness Platform",
    ]

    for item in roadmap:

        st.write(f"• {item}")

    st.divider()

    st.success(
        "Research programme currently under active development through Enet Technologies."
    )
