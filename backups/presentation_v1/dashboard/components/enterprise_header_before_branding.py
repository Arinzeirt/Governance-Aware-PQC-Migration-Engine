import streamlit as st


def show():

    left, right = st.columns([8, 2])

    with left:

        st.markdown(
            """
### ENET TECHNOLOGIES

##### Enterprise Quantum Migration Platform

Governance-Aware Post-Quantum Migration
"""
        )

    with right:

        st.success("● LIVE")

        st.caption("Version 2.0 DEV")

    st.divider()

