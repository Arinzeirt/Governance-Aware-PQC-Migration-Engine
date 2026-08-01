import streamlit as st


def show():

    st.title("Research Centre")

    st.caption(
        "Enterprise Quantum Migration Platform • Research & Innovation"
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

    st.success("Governance-Aware PQC Migration Framework")

    st.success("Enterprise Quantum Readiness Framework")

    st.success("Migration Decision Engine")

    st.success("Cryptographic Discovery & Inventory Model")

    st.divider()

    st.subheader("Research Notes")

    st.info("Enterprise Research Notes Series")

    st.info("Post-Quantum Migration Insights")

    st.info("Governance & Cryptographic Agility")

    st.info("Enterprise Architecture for PQC")

    st.divider()

    st.subheader("Publications")

    st.info("Journal Publications")

    st.info("Conference Papers")

    st.info("Technical Reports")

    st.info("White Papers")

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
