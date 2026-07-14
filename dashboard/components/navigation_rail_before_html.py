import streamlit as st


def show():

    with st.sidebar:

        st.markdown(
            """
# ENET

Enterprise Quantum Migration Platform
"""
        )

        st.divider()

        st.caption("EXECUTIVE WORKSPACE")

        st.button("Dashboard", use_container_width=True)
        st.button("Assessment", use_container_width=True)
        st.button("Inventory", use_container_width=True)
        st.button("Reports", use_container_width=True)
        st.button("Migration Planner", use_container_width=True)

        st.divider()

        st.caption("ENGINEERING")

        st.button("Repository Explorer", use_container_width=True)
        st.button("Architecture", use_container_width=True)
        st.button("Developer Portal", use_container_width=True)

        st.divider()

        st.caption("RESEARCH")

        st.button("Research Centre", use_container_width=True)
        st.button("Research Notes", use_container_width=True)
        st.button("Frameworks & Publications", use_container_width=True)

        st.divider()

        st.caption("ABOUT")

        st.button("About EQMP", use_container_width=True)
        st.button("Research Portfolio", use_container_width=True)

        st.divider()

        st.caption("Version 2.0 DEV")
        st.caption("© Enet Technologies")
