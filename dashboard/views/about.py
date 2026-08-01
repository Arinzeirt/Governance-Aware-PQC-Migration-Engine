import streamlit as st


def show():

    st.title("About")

    st.caption(
        "Enterprise Quantum Migration Platform • Enet Technologies"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Platform",
            "EQMP"
        )

    with col2:
        st.metric(
            "Version",
            "v1.0"
        )

    with col3:
        st.metric(
            "Organization",
            "Enet"
        )

    with col4:
        st.metric(
            "Research",
            "Active"
        )

    st.divider()

    st.subheader("About the Enterprise Quantum Migration Platform")

    st.write("""
The Enterprise Quantum Migration Platform (EQMP) is a governance-aware
assessment platform developed to support enterprise adoption of
post-quantum cryptography.

EQMP combines cryptographic discovery, governance, migration planning,
risk assessment and executive reporting into a single enterprise
decision-support platform for organizations preparing for the
post-quantum era.
""")

    st.divider()

    st.subheader("About Enet Technologies")

    st.write("""
Enet Technologies is a cybersecurity and secure systems engineering
company focused on enterprise resilience, governance, and emerging
security technologies.

The organization develops practical tools and research-driven
solutions that help organizations improve cyber resilience while
preparing for future technological change.
""")

    st.divider()

    st.subheader("Research Focus")

    st.write("""
Current research focuses on:

• Governance-aware PQC migration

• Enterprise cryptographic discovery

• Cryptographic agility

• Executive decision support

• AI-assisted migration planning

• Enterprise quantum readiness
""")

    st.divider()

    st.subheader("Platform Vision")

    st.info(
        "Enable organizations to migrate toward quantum-safe cryptography through governance, automation and evidence-based decision support."
    )

    st.divider()

    st.subheader("Collaboration")

    st.write("""
EQMP is intended to support collaboration between:

• Government agencies

• Financial institutions

• Critical infrastructure operators

• Researchers

• Universities

• Industry partners
""")

    st.divider()

    st.subheader("Project Information")

    st.code(
"""Enterprise Quantum Migration Platform (EQMP)

Developed by:
Enet Technologies

Research Area:
Governance-Aware Post-Quantum Cryptographic Migration

Current Release:
v1.0 Presentation"""
    )
