import streamlit as st


GITHUB_URL = "https://github.com/Arinzeirt/Governance-Aware-PQC-Migration-Engine"

CLONE_COMMAND = (
    "git clone "
    "git@github.com:Arinzeirt/Governance-Aware-PQC-Migration-Engine.git"
)


def show():

    st.title("Enterprise Repository")

    st.caption(
        "Governance-Aware PQC Migration Engine • Technical Review Portal"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Release",
            "v1.0 Presentation"
        )

    with col2:
        st.metric(
            "Status",
            "Active"
        )

    with col3:
        st.metric(
            "Organization",
            "Enet Technologies"
        )

    with col4:
        st.metric(
            "Research",
            "PQC Migration"
        )

    st.divider()

    st.subheader("Project Overview")

    st.write(
        """
The Enterprise Quantum Migration Platform (EQMP) is a governance-aware
post-quantum cryptographic migration platform designed to help
organizations discover cryptographic assets, generate enterprise
inventories, assess migration readiness, and support structured
post-quantum transition planning.

The platform combines technical discovery with governance,
risk management, compliance, and executive reporting to
support enterprise-scale migration programmes.
"""
    )

    st.divider()

    st.subheader("Technology Stack")

    c1, c2, c3, c4 = st.columns(4)

    c1.success("Python")
    c2.success("Streamlit")
    c3.success("Plotly")
    c4.success("ReportLab")

    c5, c6, c7, c8 = st.columns(4)

    c5.success("Typer")
    c6.success("Git")
    c7.success("PQC")
    c8.success("Enterprise Architecture")

    st.divider()

    st.subheader("Git Repository")

    st.code(
        GITHUB_URL,
        language="text"
    )

    st.subheader("Clone Repository")

    st.code(
        CLONE_COMMAND,
        language="bash"
    )

    st.divider()

    st.subheader("Documentation")

    st.info("Architecture Documentation (Coming Soon)")
    st.info("Research Publications (Coming Soon)")
    st.info("Migration Framework (Coming Soon)")
    st.info("Developer Documentation (Coming Soon)")

    st.divider()

    st.subheader("Repository Status")

    st.success(
        "The EQMP research prototype is under active development."
    )
