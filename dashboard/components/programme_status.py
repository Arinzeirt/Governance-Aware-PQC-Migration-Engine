import streamlit as st


def show():

    st.subheader("Research Programme")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Research Status",
                "Active"
            )

            st.metric(
                "Current Phase",
                "Research Foundation"
            )

            st.metric(
                "Expected Completion",
                "2030"
            )

        with col2:

            st.metric(
                "Institution",
                "MMU"
            )

            st.metric(
                "Platform",
                "EQMP"
            )

            st.metric(
                "Research Assets",
                "23+"
            )

        st.divider()

        st.caption(
            "Adaptive and Governance-Aware Post-Quantum Cryptographic Migration for High-Throughput Financial Systems."
        )
