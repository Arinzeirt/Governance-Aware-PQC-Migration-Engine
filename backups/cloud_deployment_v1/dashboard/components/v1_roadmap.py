import streamlit as st


def show():

    st.subheader("Executive Roadmap")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.success("""
### Immediate

• Inventory Assets

• Identify Critical Systems

• Establish Governance
""")

    with c2:

        st.info("""
### 30 Days

• Review PKI

• ML-KEM Pilot

• Update Policies
""")

    with c3:

        st.warning("""
### 90 Days

• Phase 1 Rollout

• Compliance Review

• Migration Planning
""")
