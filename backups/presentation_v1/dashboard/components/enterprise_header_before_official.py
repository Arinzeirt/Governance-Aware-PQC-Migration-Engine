import streamlit as st


def show():

    left, center, right = st.columns([6, 3, 2])

    with left:

        st.markdown(
            """
## ENET TECHNOLOGIES

**Enterprise Quantum Migration Platform**

*Governance-Aware Post-Quantum Cryptographic Migration*
"""
        )

    with center:

        st.info("Enterprise Workspace")

    with right:

        st.success("● LIVE")

        st.caption("Version 2.0 DEV")

    st.divider()
