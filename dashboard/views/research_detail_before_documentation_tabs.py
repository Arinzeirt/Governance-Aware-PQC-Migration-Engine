import streamlit as st


RESEARCH = {

    "Governance-Aware PQC Migration Framework": {

        "status": "Active Research",

        "institution": "Manchester Metropolitan University",

        "summary":
        """
The Governance-Aware PQC Migration Framework provides a structured
approach for enterprise migration to post-quantum cryptography.

It combines governance, cryptographic discovery, enterprise
architecture and migration planning into a single methodology.
""",

    },

    "Enterprise Quantum Readiness Framework": {

        "status": "Framework Development",

        "institution": "Enet Technologies",

        "summary":
        """
A maturity model used to evaluate how prepared an organisation is
for migration to post-quantum cryptography.
""",

    },

    "Migration Decision Engine": {

        "status": "Prototype",

        "institution": "Enet Technologies",

        "summary":
        """
A governance-aware decision engine that prioritises cryptographic
migration activities using business impact, governance and risk.
""",

    },

    "Cryptographic Discovery & Inventory Model": {

        "status": "Prototype",

        "institution": "Enet Technologies",

        "summary":
        """
A discovery methodology for identifying cryptographic assets,
dependencies and migration priorities across enterprise systems.
""",

    },

}


def show():

    item = st.session_state.get(
        "research_item",
        "Research"
    )

    info = RESEARCH.get(item)

    st.title(item)

    st.caption(
        "Enterprise Quantum Migration Platform • Research Detail"
    )

    st.divider()

    if info is None:

        st.warning(
            "Research content is currently unavailable."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Status",
                info["status"]
            )

        with col2:

            st.metric(
                "Institution",
                info["institution"]
            )

        st.write("")

        st.subheader("Overview")

        st.write(info["summary"])

        st.divider()

        st.subheader("Resources")

        st.info(
            "Framework documentation and downloadable resources will appear here."
        )

    st.write("")

    if st.button(
        "← Back to Research Centre",
        use_container_width=True
    ):

        st.session_state.page = "research"

        st.rerun()
