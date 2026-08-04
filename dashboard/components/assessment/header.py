import streamlit as st


def show():

    st.markdown(
        """
<h1 style="
margin-bottom:6px;
font-size:40px;
font-weight:700;
color:white;
">
Enterprise Quantum Readiness Assessment
</h1>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div style="
font-size:17px;
line-height:1.8;
color:#AEBFD5;
margin-bottom:18px;
max-width:850px;
">
Configure your organisation for a governance-aware
post-quantum readiness assessment.
</div>
""",
        unsafe_allow_html=True,
    )

    st.caption("Estimated Completion Time: 4–6 minutes")

    st.divider()
