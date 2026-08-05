import streamlit as st

from components.landing.footer import show as show_footer


def show():

    #
    # Hero
    #

    st.title("About the Enterprise Quantum Migration Platform")

    st.caption(
        "Governance • Research • Innovation • Enterprise Security"
    )

    st.markdown(
        """
<div style="
background:#111827;
border:1px solid #334155;
border-radius:16px;
padding:36px;
margin-top:20px;
margin-bottom:30px;
">

<div style="
font-size:14px;
font-weight:700;
color:#60A5FA;
margin-bottom:10px;
">
ABOUT EQMP
</div>

<div style="
font-size:34px;
font-weight:700;
line-height:1.35;
color:white;
margin-bottom:18px;
">

Building Enterprise Confidence
for the Post-Quantum Era

</div>

<div style="
font-size:16px;
line-height:1.9;
color:#CBD5E1;
">

The Enterprise Quantum Migration Platform (EQMP) is a governance-aware
platform designed to help organisations prepare for the transition to
post-quantum cryptography. By combining research, enterprise architecture,
governance and cryptographic intelligence, EQMP enables organisations to
understand their current security posture, prioritise migration activities
and build long-term quantum resilience.

</div>

</div>
""",
        unsafe_allow_html=True,
    )

    #
    # Mission & Vision
    #

    left, right = st.columns(2, gap="large")

    with left:

        st.info(
            """
### 🎯 Our Mission

To empower organisations with practical,
governance-driven solutions that simplify
the journey toward post-quantum security
while strengthening enterprise cyber
resilience.
"""
        )

    with right:

        st.info(
            """
### 🚀 Our Vision

To become the trusted enterprise platform
advancing post-quantum readiness across
governments, critical infrastructure and
industry through research, innovation and
strategic collaboration.
"""
        )

    st.divider()

    #
    # About Enet
    #

    st.subheader("About Enet Technologies")

    st.markdown(
        """
Enet Technologies is a cybersecurity and secure systems engineering
company committed to building innovative technologies that strengthen
enterprise resilience.

Through applied research, engineering excellence and strategic
collaboration, we develop practical solutions that help organisations
prepare for emerging security challenges while enabling secure digital
transformation.
"""
    )

    st.divider()

    #
    # Partnerships
    #

    st.subheader("Strategic Partnerships")

    st.markdown(
        """
EQMP is built on the belief that meaningful innovation is achieved
through collaboration.

We actively welcome partnerships with organisations that share our
vision of advancing enterprise cybersecurity and accelerating the
adoption of post-quantum security.

Our collaboration ecosystem includes:

- Government & Public Sector Organisations
- Financial Institutions
- Critical Infrastructure Operators
- Universities & Research Institutions
- Technology & Cloud Providers
- Standards & Regulatory Bodies
- Enterprise Security Teams
- Industry & Innovation Partners
"""
    )

    st.divider()

    #
    # Commitment
    #

    st.success(
        """
### Our Commitment

We are committed to advancing enterprise cybersecurity through
research, innovation and responsible technology development,
helping organisations prepare confidently for the quantum era.
"""
    )

    st.divider()

    show_footer()

